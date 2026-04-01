from etl.models import ETLConfig
from etl.extract.extract_adapter import ExtractAdapter
from jobspy import scrape_jobs

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
