import pandas as pd
from abc import ABC, abstractmethod
from models import PipelineContext

class ExtractAdapter(ABC):
    """
    This class allows to use the design pattern Adapter.
    It makes easy to use some library or API for ETL classes
    """
    @staticmethod
    @abstractmethod
    def request(context: PipelineContext):
        pass

    @staticmethod
    @abstractmethod
    def to_dataframe(data) -> pd.DataFrame:
        pass