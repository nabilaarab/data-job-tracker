from etl.etl_job_offers import ETLJobOffers
from etl.extract.extract_adapter_api_job_cloud import ExtractAdapterAPIJobCloud
from etl.models import ETLConfig
import pandas as pd


# Get config.txt
# etl_config = ETLConfig.load_config()
# print(etl_config)


# etl_joboffers = ETLJobOffers()
# etl_joboffers.run_all()

# Try analysis

from analysis.models import AnalyzerConfig
from analysis.analyzer_llm import AnalyzerLLM
from utils import read_file

analyzer_config = AnalyzerConfig(
        [],
        ai_model="llama-3.1-8b-instant",
        prompt_system_content=(
            "Tu es un expert en recrutement. Tu vas recevoir les mots-clés d'un CV et une fiche de poste. "
            "Évalue les chances de ce CV en donnant un score de pertinence allant de 0 à 100. "
            "Réponds UNIQUEMENT avec ce JSON, sans texte avant ni après : {\"score\": <entier 0-100>}"
        ),
        prompt_user_content=(
            "Voici le CV : {resume}" \
            "\n\nVoici la fiche de poste : {job_description}"
        ),
        #prompt_output_desired="json_object"
        prompt_output_desired={
            "type": "json_object"
        }
        # prompt_output_desired=None
)

analyzer_config.prompt_user_content = analyzer_config.prompt_user_content.format(
    resume=read_file("analysis/input/resume.local.txt"),
    job_description=read_file("analysis/input/description.txt")
)

analyzer_llm = AnalyzerLLM(analyzer_config)
analyzer_llm.run()
