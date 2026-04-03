import pandas as pd
from abc import ABC, abstractmethod
from etl.models import ETLConfig

class ExtractAdapter(ABC):
    """
    This class allows to use the design pattern Adapter.
    It makes easy to use some library or API for ETL classes
    """
    @staticmethod
    @abstractmethod
    def request(etl_config: ETLConfig):
        pass

    @staticmethod
    @abstractmethod
    def to_dataframe(data) -> pd.DataFrame:
        pass