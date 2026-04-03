import logging
import pandas as pd
import random
from datetime import datetime, timedelta
from etl.extract.constants import JOBCLOUD__REGION_IDS
from etl.extract.extract_adapter import ExtractAdapter
from etl.models import ETLConfig
from typing import Any, Dict, List, Optional
from etl.extract.utils import requests_with_retry

logger = logging.getLogger(__name__)


class ExtractAdapterAPIJobCloud(ExtractAdapter):
    """
    This class makes easy to use the API of the company JobCloud which can get data from Jobs.ch or Jobup.ch
    """
    __HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/115.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive"
    }
    
    # function: request ------------------------------------------------------------------------
    @staticmethod
    def request(
        etl_config:     ETLConfig,
        location:       str, 
        key_word:       str,
        fetch_jobup:    bool = True,
        fetch_jobs:     bool = True
    ) -> pd.DataFrame:
        """
        """
        location = location.lower()
        # WE CHECK IF IT IS A LOCATION KNOWN
        if location not in JOBCLOUD__REGION_IDS:
            # IF NOT, WE CANNOT MANAGE THIS REQUEST
            print("Lieu inconnu ou pas en Suisse.")
            return None
        
        # BUILD CONFIG IN FUNCTION OF WHAT WE HAVE IN PARAMETERS
        fetch_websitedata_config = {}

        if fetch_jobup:
            fetch_websitedata_config["JOBUP"] = {
                "url_search": "https://job-search-api.jobup.ch/search/semantic",
                "url_detail": "https://www.jobup.ch/api/v1/public/search/job/{id_job}"
            }

        if fetch_jobs:
            fetch_websitedata_config["JOBS"] = {
                "url_search": "https://job-search-api.jobs.ch/search/semantic",
                "url_detail": "https://www.jobs.ch/api/v1/public/search/job/{id_job}"
            }

        all_offers = {}
        for website in fetch_websitedata_config:
            # REQUEST OFFERS DETAILS IN THE SELECTED WEBSITE
            offers_details = ExtractAdapterAPIJobCloud._request_one_websitedata(
                etl_config,
                location,
                key_word,
                fetch_websitedata_config[website]["url_search"],
                fetch_websitedata_config[website]["url_detail"],
            )
            
            all_offers[website] = offers_details

        return all_offers


    # function: _request_one_websitedata ------------------------------------------------------------
    @staticmethod
    def _request_one_websitedata(
        etl_config:     ETLConfig,
        location:       str, 
        key_word:       str,
        url_search:     str,
        url_detail:     str
    ):
        # GET ALL JOBS
            response = ExtractAdapterAPIJobCloud._request_get_list_offers(
                etl_config,
                location,
                key_word,
                url_search
            )

            # IF WE CANNOT GET OFFERS, WE STOP IT
            if response is None:
                return None
            resp = response.json()
            
            # GET ids
            docs = resp["documents"]
        
            # LAUNCH JOBS EXPLORATION
            offers_details = []
            for doc in docs:
                id_job = doc["id"]
                print(id_job)
                offer_detail = ExtractAdapterAPIJobCloud._request_get_offer_detail(
                    url_detail,
                    id_job,
                    etl_config.proxies
                )
                offers_details.append(offer_detail.json())

            print(f"Il y a eu {len(offers_details)} offres trouvées !")

            return offers_details

    # function: _request_get_list_offers ------------------------------------------------------------
    @staticmethod
    def _request_get_list_offers(
            etl_config: ETLConfig,
            location:   str,
            key_word:   str,
            url_api:    str
        ):
        """_summary_

        Args:
            etl_config (ETLConfig): _description_
            location (str): _description_
            key_word (str): _description_
            url_api (str): _description_

        Returns:
            _type_: _description_
        """
        # BUILD VARIABLES
        region_id = JOBCLOUD__REGION_IDS[location]

        rows = min(300, etl_config.max_results_per_platform)

        params = ExtractAdapterAPIJobCloud._build_params(
            key_word,
            location, 
            region_id, 
            rows,
            etl_config.posted_within_days
            )
        
        proxies = ExtractAdapterAPIJobCloud._build_proxies(etl_config.proxies)
        
        # LAUNCH AND RETURN REQUEST
        return requests_with_retry(
            url_api,
            headers=ExtractAdapterAPIJobCloud.__HEADERS,
            params=params,
            proxies=proxies,
            logger=logger
        )
    
    # function: _request_get_offer_detail ------------------------------------------------------------
    @staticmethod
    def _request_get_offer_detail(
        url_api:    str,
        id_job:   str,
        proxies:    List[str]    
        ):
        """_summary_

        Args:
            url_api (str): _description_
            id_offer (str): _description_
            proxies (List[str]): _description_

        Returns:
            _type_: _description_
        """

        # GET VARIABLES
        url_complete = url_api.format(id_job=id_job)
        proxies = ExtractAdapterAPIJobCloud._build_proxies(proxies)


        # LAUNCH AND RETURN REQUEST
        return requests_with_retry(
            url_complete,
            headers=ExtractAdapterAPIJobCloud.__HEADERS,
            proxies=proxies,
            logger=logger
        )

    # function: _build_params ------------------------------------------------------------------------
    @staticmethod
    def _build_params(
        query:              str,
        location:           str,
        region_id:          int,
        rows:               int,
        posted_within_days: int | None
        ) -> dict:
        """_summary_

        Args:
            query (str): _description_
            location (str): _description_
            region_id (int): _description_
            rows (int): _description_
            posted_within_days (int | None): _description_

        Returns:
            dict: _description_
        """
        # Create base parameters
        params: Dict[str, Any]  = {
            "query": query,
            "location": location,
            "regionsIds": region_id,
            "rows": rows
        }

        # Add parameters of date if necessary
        if posted_within_days is not None:
            date_to     = datetime.now()
            date_from   = date_to - timedelta(days=posted_within_days)
            params["publicationDateFrom"] = date_from.strftime("%Y-%m-%d 00:00:00")
            params["publicationDateTo"]   = date_to.strftime("%Y-%m-%d 23:59:59")
        
        return params
    
    # function: _build_proxies ------------------------------------------------------------------------
    @staticmethod
    def _build_proxies(proxies: List[str]) -> Optional[dict]:
        """Select randomly a proxy and return a dict compatible requests.

        Args:
            proxies (List[str]): List of proxies

        Returns:
            Optional[dict]: return a dict compatible requests
        """
        if proxies is None or len(proxies) == 0:
            return None
        proxy_chose = random.choice(proxies)
        return {
            "http": f"http://{proxy_chose}",
            "https": f"http://{proxy_chose}"
        }

    # function: to_dataframe ------------------------------------------------------------------------
    @staticmethod
    def to_dataframe(data) -> pd.DataFrame:
        """This function get the result of the request and transform it in DataFrame

        Args:
            data (_type_): _description_

        Returns:
            pd.DataFrame: _description_
        """
        # CONVERT TO DATAFRAME
        dfs = []
        for website in data:
            data_website_selected =  data[website]

            df_website_selected = pd.DataFrame(data_website_selected)
            df_website_selected["site"] = website

            dfs.append(df_website_selected)

        df_merged: pd.DataFrame = pd.concat(dfs)

        for column in df_merged.columns:
            print(column)



        # BUILD VARIABLES
        df["location"] = df_merged["locations"]["street"] + df_merged["locations"]["postalCode"]+ df_merged["locations"]["city"]
        df["location"] += df_merged["locations"]["cantonCode"] + df_merged["locations"]["countryCode"]

        # RENAME COLUMNS
        df_final = pd.DataFrame(
            {
                "id": df_merged["job_id"],
                "site": df_merged["site"],
                "job_url": df_merged["_links"]["detail_fr"]["href"],
                "job_url_direct": None, 
                "title": df_merged["title"],
                "company": df_merged["company_name"],
                "location": df_merged["location"],
                "date_posted": df_merged["publication_end_date"],
                "job_type": df_merged["site"],
                "is_remote": df_merged["site"],
                "job_level": df_merged["site"],
                "job_function": df_merged["site"],
                "emails": df_merged["site"],
                "description": df_merged["site"],
                "company_url": df_merged["site"],
                "company_url_direct": df_merged["site"],
                "company_addresses": df_merged["site"],
                "company_num_employees": df_merged["site"],
                "company_description": df_merged["site"],
            }
        )


        return df
