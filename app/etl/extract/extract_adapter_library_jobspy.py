import pandas as pd
from etl.models import ETLConfig
from etl.extract.extract_adapter import ExtractAdapter
from jobspy import scrape_jobs

class ExtractAdapterLibraryJobSpy(ExtractAdapter):
    """
    This class makes Easy to use the Library JobSpy and then get job offers from Linkedin or Indeed.
    """

    # function: request ------------------------------------------------------------------------
    @staticmethod
    def request(etl_config: ETLConfig):
        results = []
        for location in etl_config.locations:
            for key_word in etl_config.key_words:
                print(f"[LibraryJobSpy] Search {key_word} in {location}...")

                jobs_location_keyword = scrape_jobs(
                    site_name=etl_config.site_names,
                    search_term=key_word,
                    location=location,
                    country_indeed=etl_config.location_countries[location],
                    results_wanted=etl_config.max_results_per_platform,
                    hours_old=24 * etl_config.posted_within_days,
                    linkedin_fetch_description=True,
                    proxies=etl_config.proxies,
                )
                results.append(jobs_location_keyword)
        
        return results
        # return pd.concat(results, ignore_index=True)
    
    # function: to_dataframe -------------------------------------------------------------------
    @staticmethod
    def to_dataframe(data) -> pd.DataFrame:
        return data