import pandas as pd
import random
import requests
from datetime import datetime, timedelta
from etl.extract.constants import JOBCLOUD__REGION_IDS
from etl.extract.extract_adapter import ExtractAdapter
from etl.models import ETLConfig
from typing import Any, Dict, List, Optional
from utils import requests_with_retry

class ExtractAdapterAPIJobCloud(ExtractAdapter):
    """
    This class makes easy to use the API of the company JobCloud which can get data from Jobs.ch or Jobup.ch
    """
    _URL = None
    _HEADERS = None
    _PARAMS = None
    
    # request function ------------------------------------------------------------------------
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
        pass
        

    # _build_params function ------------------------------------------------------------------------
    @staticmethod
    def _build_params(
        location:           str,
        region_id:          int,
        rows:               int,
        start:              int,
        posted_within_days: int | None
        ) -> dict:
        """_summary_

        Args:
            location (str): _description_
            region_id (int): _description_
            rows (int): _description_
            start (int): _description_
            posted_within_days (int | None): _description_

        Returns:
            dict: _description_
        """
        # Create base parameters
        params: Dict[str, Any]  = {
            "location": location,
            "regionsIds": region_id,
            "rows": rows,
            "start": start
        }

        # Add parameters of date if necessary
        if posted_within_days is not None:
            date_to     = datetime.now()
            date_from   = date_to - timedelta(days=posted_within_days)
            params["publicationDateFrom"] = date_from.strftime("%Y-%m-%d 00:00:00")
            params["publicationDateTo"]   = date_to.strftime("%Y-%m-%d 23:59:59")
        
        return params
    
    # _build_proxy function ------------------------------------------------------------------------
    @staticmethod
    def _build_proxy(proxies: List[str]) -> Optional[dict]:
        """Select randomly a proxy and return a dict compatible requests.

        Args:
            proxies (List[str]): List of proxies

        Returns:
            Optional[dict]: return a dict compatible requests
        """
        proxy_chose = random.choice(proxies)
        return {
            "http": f"http://{proxy_chose}",
            "https": f"http://{proxy_chose}"
        }
        


class ExtractAdapterAPIJobUp(ExtractAdapterAPIJobCloud):
    pass
