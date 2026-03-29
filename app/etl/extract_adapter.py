import pandas as pd
import requests
from abc import ABC, abstractmethod
from jobspy import scrape_jobs
from etl.models import ETLConfig

class ExtractAdapter(ABC):
    """
    This class allows to use the design pattern Adapter.
    It makes easy to use some library or API for ETL classes
    """
    @staticmethod
    @abstractmethod
    def request(etl_config: ETLConfig) -> pd.DataFrame:
        pass


class ExtractAdapterLibraryJobSpy(ExtractAdapter):
    """
    This class makes Easy to use the Library JobSpy and then get job offers from Linkedin or Indeed.
    """
  
    @staticmethod
    def request(etl_config: ETLConfig, location:str, key_word:str):
        return scrape_jobs(
            site_name=etl_config.site_names,
            search_term=key_word,
            location=location,
            country_indeed=etl_config.location_countries[location],
            results_wanted=etl_config.max_results_per_platform,
            hours_old=24 * etl_config.posted_within_days,
            linkedin_fetch_description=True,
            proxies=etl_config.proxies,
        )


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
