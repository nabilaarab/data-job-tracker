import pandas as pd
import requests
from etl.models import ETLConfig
from etl.extract.extract_adapter import ExtractAdapter

class ExtractAdapterAPIJobCloud(ExtractAdapter):
    """
    This class makes easy to use the API of the company JobCloud which can get data from Jobs.ch or Jobup.ch
    """
    _URL = None
    _HEADERS = None
    _PARAMS = None
    
    @staticmethod
    def request(
        etl_config: ETLConfig,
        location:str, 
        key_word:str
    ) -> pd.DataFrame:
        """
        """
        response = requests.get(
            ExtractAdapterAPIJobCloud._URL, 
            headers=ExtractAdapterAPIJobCloud._HEADERS, 
            params=ExtractAdapterAPIJobCloud._PARAMS
        )

class ExtractAdapterAPIJobUp(ExtractAdapterAPIJobCloud):
    """
    """
    pass
