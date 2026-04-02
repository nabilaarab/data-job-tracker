import pandas as pd
import requests
from datetime import datetime, timedelta
from etl.extract.extract_adapter import ExtractAdapter
from etl.models import ETLConfig
from typing import Any, Dict

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
        location:   str, 
        key_word:   str
    ) -> pd.DataFrame:
        """
        """
        response = requests.get(
            ExtractAdapterAPIJobCloud._URL, 
            headers=ExtractAdapterAPIJobCloud._HEADERS, 
            params=ExtractAdapterAPIJobCloud._PARAMS
        )

    @staticmethod
    def _build_params(
        location:           str,
        region_id:          int,
        rows:               int,
        start:              int,
        posted_within_days: int | None
        ) -> dict:
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

class ExtractAdapterAPIJobUp(ExtractAdapterAPIJobCloud):
    pass