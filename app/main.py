from etl.etl_job_offers import ETLJobOffers
from etl.extract.extract_adapter_api_job_cloud import ExtractAdapterAPIJobCloud
from etl.utils import load_config
import pandas as pd


# Get config.txt
etl_config = load_config()
print(etl_config)


etl_joboffers = ETLJobOffers()
etl_joboffers.run_all()




# print(res)


# etl_adapter = ExtractAdapterAPIJobCloud()
# res = etl_adapter.request(etl_config, "Lausanne", "Data Engineer")
# res = etl_adapter.to_dataframe(res)
# print(res)

# print("LAUNCH ---")
# print(type(res))
# print(res)



# etl_joboffers = ETLJobOffers()

# etl_joboffers.run_all()





# from dags.etl_job_offers import etl_job_offers_pipeline

# etl_job_offers_pipeline()
