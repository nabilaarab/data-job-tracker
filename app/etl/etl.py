import pandas as pd
from abc import ABC, abstractmethod
from etl.extract.extract_adapter_api_job_cloud import ExtractAdapterAPIJobCloud
from etl.extract.extract_adapter_library_jobspy import ExtractAdapterLibraryJobSpy
from etl.load.load_strategy import LoadStrategy
from etl.load.load_strategy_excel import LoadStrategyExcel
from typing import List


class ETL(ABC):
    """
    It is an abstract class which explain the behavior of an ETL.
    """
    def __init__(self):
        self.loader_strategies: List[LoadStrategy] = [LoadStrategyExcel]

    @abstractmethod
    def extract(self):
        pass

    @abstractmethod
    def transform(self):
        pass

    @abstractmethod
    def load(self):
        pass

    def run_all(self):
        """
        run extract then transform then load.
        """
        data_extracted = self.extract()
        data_transformed = self.transform(data_extracted)
        self.load(data_transformed)
