from analysis.analyzer_llm import AnalyzerLLM
from analysis.models import AnalyzerConfig
from pipeline_config import LLM_MODEL, LLM_PROMPT_OUTPUT, LLM_PROMPT_SYSTEM, LLM_PROMPT_USER
from utils import read_file

class Pipeline:
    """This class allows you to scrape the data, analyze and use them."""
    def launch_etl():
        pass

    def launch_analyzer():
        analyzer_config = AnalyzerConfig(
            [],
            ai_model=LLM_MODEL,
            prompt_system_content=LLM_PROMPT_SYSTEM,
            prompt_user_content=LLM_PROMPT_USER,
            prompt_output_desired=LLM_PROMPT_OUTPUT
        )

        analyzer_config.prompt_user_content = analyzer_config.prompt_user_content.format(
            resume=read_file("analysis/input/resume.local.txt"),
            job_description=read_file("analysis/input/description.txt")
        )

        analyzer_llm = AnalyzerLLM(analyzer_config)
        analyzer_llm.run()
