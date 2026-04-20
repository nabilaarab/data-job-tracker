from abc import ABC, abstractmethod
from analysis.analyzer import AnalyzerConfig, AnalyzerKeyWord, AnalyzerLLM
from etl.extract.extract_adapter import ExtractAdapter
from etl.extract.extract_adapter_api_job_cloud import ExtractAdapterAPIJobCloud
from etl.extract.extract_adapter_library_jobspy import ExtractAdapterLibraryJobSpy
from etl.load.load_strategy_excel import LoadStrategyExcel
from lxml import html
from models import PipelineContext
from pipeline_config import LLM_MODEL, LLM_PROMPT_OUTPUT, LLM_PROMPT_SYSTEM, LLM_PROMPT_USER
from typing import cast
from utils import get_latest_file, load_key_words, read_file
import json
import pandas as pd

# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #
class PipelineStep(ABC):
    @classmethod
    @abstractmethod
    def run(cls, context: PipelineContext):
        pass

    @staticmethod
    def _get_latest_jobs(path_folder: str = "etl/output/") -> pd.DataFrame:
        return pd.read_excel(get_latest_file(path_folder))

class PipelineStepInitContextJobOffers(PipelineStep):
    @classmethod
    def run(cls, context: PipelineContext):
        return PipelineContext.load_config()

# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #
class PipelineStepExtractJobOffers(PipelineStep):
    @classmethod
    def run(cls, context: PipelineContext):
        extractors = [
            ExtractAdapterAPIJobCloud,
            ExtractAdapterLibraryJobSpy
        ]

        data = {}
        for extract_method in extractors:
            extract_method: ExtractAdapter
            res = extract_method.request(context)

            data[extract_method] = res

        context.data = data

        return context

# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #
class PipelineStepTransformJobOffers(PipelineStep):
    def run(cls, context: PipelineContext):
        """_summary_

        Args:
            config (PipelineConfig): _description_
            data (_type_): Data you want to transform

        Returns:
            _type_: _description_
        """
        extractors = [
            ExtractAdapterAPIJobCloud,
            ExtractAdapterLibraryJobSpy
        ]
        data = []
        for extractor in extractors:
            extractor: ExtractAdapter
            data_to_transform = context.data.get(extractor)
            print("ici")
            print(type(data_to_transform))
            print(len(data_to_transform))
            print(data_to_transform)
            # IF THE SOURCE IS THE JOBSPY LIBRARY
            if extractor == ExtractAdapterLibraryJobSpy:
                data_to_transform = pd.concat(data_to_transform, ignore_index=True)
            
            # IF THE SOURCE IS THE JOBCLOUD API
            print(ExtractAdapterAPIJobCloud)
            print(extractor)
            if extractor == ExtractAdapterAPIJobCloud:
                dfs = []
                for i in range(0, len(data_to_transform)):
                    df = cls.__to_dataframe_reply_api_jobcloud(data_to_transform[i])
                    dfs.append(df)

                data_to_transform = pd.concat(dfs, ignore_index=True)

            data.append(data_to_transform)
        
        # MERGE THE DATAFRAMES
        df = cast(pd.DataFrame, pd.concat(data, ignore_index=True))

        # REMOVE DUPLICATES
        print("Suppression des doublons...")
        df_duplicates_dropped = df.drop_duplicates(subset=["id"])

        # PRINT THE NUMBER OF DROPPED RAWS
        count_dropped_lines = len(df) - len(df_duplicates_dropped)
        print(f"{count_dropped_lines} doublon(s) supprimé(s)")

        context.data = df

        return context
    
    # function: to_dataframe ------------------------------------------------------------------------
    # WARNING : split this functions ! Too much responsability
    @classmethod
    def __to_dataframe_reply_api_jobcloud(cls, data) -> pd.DataFrame:
        """This function get the result of the request and transform it in DataFrame

        Args:
            data (_type_): _description_

        Returns:
            pd.DataFrame: _description_
        """
        # CONVERT TO DATAFRAME
        dfs = []
        for website in data:
            data_website_selected =  data[website]

            df_website_selected = pd.DataFrame(data_website_selected)
            df_website_selected["site"] = website

            dfs.append(df_website_selected)

        df_merged: pd.DataFrame = pd.concat(dfs)


        # GET LOCATIONS
        from_series_jobs_locations = df_merged["locations"].tolist()
        
        jobs_locations = []
        for from_series_job_locations in from_series_jobs_locations:
            job_locations = []
            str_locations = ""
            for dict_location in from_series_job_locations:
                for key in dict_location:
                    str_locations += str(dict_location[key]) + " "
                job_locations.append(str_locations)

            jobs_locations.append(job_locations)

        #print(jobs_locations)

        # GET URL
        _links_list = df_merged["_links"].tolist()

        urls = []
        detail_languages = ["detail_fr", "detail_en", "detail_de"]

        for _links in _links_list:
            for detail_language in detail_languages:
                if detail_language in _links:
                    urls.append(_links[detail_language]["href"])
                    break
        
        
        # RENAME COLUMNS
        df_final = pd.DataFrame(
            {
                "id": df_merged["job_id"],
                "site": df_merged["site"],
                "job_url": urls,
                "title": df_merged["title"],
                "description": df_merged["template_text"].apply(cls.html_to_text),
                "job_url_direct": df_merged["external_url"],
                "company": df_merged["company_name"],
                "location": jobs_locations,
                "date_posted": df_merged["last_online_date"],
                "contacts": df_merged["contacts"],
            }
        )

        return df_final

    def html_to_text(raw_html: str) -> str:
        if not raw_html:
            return ""
        tree = html.fromstring(raw_html)
        return tree.text_content().strip()
# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #
class PipelineStepLoadInExcel(PipelineStep):
    def run(cls, context: PipelineContext):
        """
        """
        LoadStrategyExcel.load(
            df=context.data
        )

        return context

# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #
class PipelineStepJobAnalyzerLLM(PipelineStep):
    @classmethod
    def run(cls, context: PipelineContext):
        df: pd.DataFrame = cls._get_latest_jobs()
        scores = []

        for row in df.itertuples():
            result = cls.__launch_one_analyzer(
                job_description=row.description
            )

            result = json.loads(result)

            result = result["score"]

            scores.append(result)
            
        df["score_llm"] = scores
        df.to_excel("analysis/output/test.xlsx", index=False)

        return context

    def __launch_one_analyzer(job_description: str):
        analyzer_config = AnalyzerConfig(
            None,
            None,
            ai_model=LLM_MODEL,
            prompt_system_content=LLM_PROMPT_SYSTEM,
            prompt_user_content=LLM_PROMPT_USER,
            prompt_output_desired=LLM_PROMPT_OUTPUT
        )

        analyzer_config.prompt_user_content = analyzer_config.prompt_user_content.format(
            resume=read_file("analysis/input/resume.local.txt"),
            # job_description=read_file("analysis/input/description.txt")
            job_description=job_description
        )

        analyzer_llm = AnalyzerLLM(analyzer_config)

        return analyzer_llm.run()

# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #
class PipelineStepJobAnalyzerKeyWords(PipelineStep):
    """This class allows you to scrape the data, analyze and use them."""

    @classmethod
    def run(cls, context: PipelineContext):
        analyzer_config = AnalyzerConfig(
            load_key_words("analysis/input/keywords.txt"),
            None,
            None,
            None,
            None,
            None
        )

        df: pd.DataFrame = cls._get_latest_jobs()
        scores = []

        analyzer = AnalyzerKeyWord(analyzer_config)
        for row in df.itertuples():
            analyzer_config.text = row.description
            result = analyzer.run()
            scores.append(result)

        df["score_keyword"] = scores
        df.to_excel("analysis/output/test_keyword.xlsx", index=False)

        return context