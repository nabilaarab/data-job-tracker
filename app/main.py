from etl.etl import ETLJobOffers
from etl.extract.extract_adapter import ExtractAdapterLibraryJobSpy
from etl.utils import load_config
import pandas as pd


# Get config.txt
# etl_config = load_config()
# print(etl_config)


# etl_adapter = ETLAdapterLibraryJobSpy()
# res: pd.DataFrame = etl_adapter.request(etl_config)

# print(type(res))
# print(res)



etl_joboffers = ETLJobOffers()

etl_joboffers.run_all()