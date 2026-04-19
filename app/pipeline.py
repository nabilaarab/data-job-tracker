from abc import ABC, abstractmethod
from analysis.analyzer import AnalyzerLLM
from analysis.models import AnalyzerConfig
from etl.etl_job_offers import ETLJobOffers
from pipeline_config import LLM_MODEL, LLM_PROMPT_OUTPUT, LLM_PROMPT_SYSTEM, LLM_PROMPT_USER
from utils import get_latest_file, read_file
import json
import pandas as pd

class Pipeline(ABC):
    @abstractmethod
    def launch_etl():
        pass

    @abstractmethod
    def launch_analyzer():
        pass

class PipelineJobOffer(Pipeline):
    """This class allows you to scrape the data, analyze and use them."""

    def launch_etl():
        etl_joboffers = ETLJobOffers()
        etl_joboffers.run_all()

    def launch_analyzer():
        df: pd.DataFrame = PipelineJobOffer.__get_latest_jobs()
        scores = []

        for row in df.itertuples():
            result = PipelineJobOffer.__launch_one_analyzer(
                job_description=row.description
            )

            result = json.loads(result)

            result = result["score"]

            scores.append(result)
            
        df["score_llm"] = scores
        df.to_excel("analysis/output/test.xlsx", index=False)
    
    def __launch_one_analyzer(job_description: str):
        analyzer_config = AnalyzerConfig(
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
    
    def __get_latest_jobs(path_folder: str = "etl/output/") -> pd.DataFrame:
        df = pd.read_excel(get_latest_file(path_folder))
        print(df)
        return df
