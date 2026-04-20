from abc import ABC, abstractmethod
from analysis.analyzer import AnalyzerConfig, AnalyzerKeyWord, AnalyzerLLM
from pipeline_config import LLM_MODEL, LLM_PROMPT_OUTPUT, LLM_PROMPT_SYSTEM, LLM_PROMPT_USER
from utils import get_latest_file, load_key_words, read_file
import json
import pandas as pd

# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #
class PipelineStep(ABC):
    @classmethod
    @abstractmethod
    def run(cls):
        pass

    @staticmethod
    def _get_latest_jobs(path_folder: str = "etl/output/") -> pd.DataFrame:
        return pd.read_excel(get_latest_file(path_folder))

# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #
class PipelineStepJobAnalyzerLLM(PipelineStep):
    @classmethod
    def run(cls):
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
    def run(cls):
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
