import logging
import requests
from typing import Optional

def requests_with_retry(
        url:            str,
        max_retries:    int = 3,
        timeout:        int = 15,
        headers:        dict[str, str]  | None  = None,
        params:         dict | None             = None, 
        proxies:        Optional[dict]          = None,
        logger:         logging.Logger | None   = None
    ):

        for i_attempt in range (1, max_retries + 1):
            # ---- TRY / EXCEPT ----
            try:
                resp = requests.get(
                    url,
                    params=params,
                    headers=headers,
                    proxies=proxies,
                    timeout=timeout
                )
                resp.raise_for_status()
                return resp
            except Exception as e:

                # IF THERE IS NOT logger, define one
                if logger is None:
                    logger = logging.getLogger(__name__)
                
                # WARNING message
                logger.warning(
                     f"Echec de la requête API - Tentative {i_attempt}/{max_retries}"
                     f"ERROR : {e}"
                     )
        
        # ERROR MESSAGE
        logger.error(f"Aucun résultat après de l'API {max_retries} tentatives.")
