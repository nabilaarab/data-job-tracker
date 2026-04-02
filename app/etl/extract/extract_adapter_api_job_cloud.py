import logging
import pandas as pd
import random
import requests
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
    _HEADERS = {
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
        etl_config: ETLConfig,
        location:   str, 
        key_word:   str
    ) -> pd.DataFrame:
        """
        """
        # WE CHECK IF IT IS A LOCATION KNOWN
        if location not in JOBCLOUD__REGION_IDS:
            # IF NOT, WE CANNOT MANAGE THIS REQUEST
            print("Lieu inconnu ou pas en Suisse.")
            return None

        response = requests.get(
            ExtractAdapterAPIJobCloud._URL, 
            headers=ExtractAdapterAPIJobCloud._HEADERS, 
            params=ExtractAdapterAPIJobCloud._PARAMS
        )

    # function: _request_get_list_offers ------------------------------------------------------------
    @staticmethod
    def _request_get_list_offers(
            etl_config: ETLConfig,
            location:   str,
            key_word:   str
        ):
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
            ExtractAdapterAPIJobCloud._URL,
            headers=ExtractAdapterAPIJobCloud._HEADERS,
            params=params,
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
        

class ExtractAdapterAPIJobUp(ExtractAdapterAPIJobCloud):
    pass
