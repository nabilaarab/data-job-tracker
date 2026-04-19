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

from pipeline import Pipeline

Pipeline.launch_analyzers()