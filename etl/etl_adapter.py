import csv
import pandas as pd
from abc import ABC, abstractmethod
from jobspy import scrape_jobs
from etl.models import ETLConfig

class ETLAdapter(ABC):
    """
    This class allows to use the design pattern Adapter.
    It makes easy to use some library or API for ETL classes
    """
    @abstractmethod
    def request(etl_config: ETLConfig) -> pd.DataFrame:
        pass


class ETLAdapterLibraryJobSpy(ETLAdapter):
    """
    This class makes Easy to use the Library JobSpy and then get job offers from Linkedin or Indeed.
    """

    def request(etl_config: ETLConfig) -> pd.DataFrame:
        results = []
        for location in etl_config.locations:
            country = etl_config.location_countries[location]

            for key_word in etl_config.key_words:
                print(f"Search {key_word} in {location}")

                jobs = scrape_jobs(
                    site_name=etl_config.site_names,
                    search_term=key_word,
                    location=location,
                    country_indeed=country,
                    results_wanted=etl_config.max_results_per_platform,
                    hours_old=24 * etl_config.posted_within_days,
                    linkedin_fetch_description=True,
                    proxies=etl_config.proxies,
                )
                results.append(jobs)
                
        return pd.concat(results, ignore_index=True)



class ETLAdapterAPIJobCloud(ETLAdapter):
    """
    This class makes easy to use the API of the company JobCloud which can get data from Jobs.ch or Jobup.ch
    """
    def request(etl_config: ETLConfig) -> pd.DataFrame:
        pass
