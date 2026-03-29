import pandas as pd
from abc import ABC, abstractmethod
from etl.etl_adapter import ETLAdapterLibraryJobSpy, ETLAdapterAPIJobCloud
from etl.etl_loader_strategy import ETLLoaderStrategy, ETLLoaderStrategyExcel
from etl.utils import load_config
from typing import List

class ETL(ABC):
    """
    It is an abstract class which explain the behavior of an ETL.
    """
    def __init__(self):
        self.loader_strategies: List[ETLLoaderStrategy] = [ETLLoaderStrategyExcel]

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


class ETLJobOffers(ETL):
    """
    The role of this ETL is to get all data related of job offers.
    """
    def __init__(self, config=None):
        super().__init__()
        self.extractors = [ETLAdapterLibraryJobSpy]

        if config is None:
            self.config = load_config()


    def extract(self):
        """
        """
        data = {}
        for extract_method in self.extractors:
            data[ETLAdapterLibraryJobSpy] = extract_method.request(self.config)

        return data

    def transform(self, data_extracted: dict):
        """
        """
        # Data treatment from JoSpy library
        data_jobspy = data_extracted.get(ETLAdapterLibraryJobSpy)
        if data_jobspy is not None:
            pass
        
        # Data treatment from JobCloud APIs
        data_jobcloud = data_extracted.get(ETLAdapterAPIJobCloud)
        if data_jobcloud is not None:
            pass

        return data_jobspy

    def load(self, df_transformed: pd.DataFrame):
        """
        """
        for loader_strategy in self.loader_strategies:
            print(type(df_transformed))
            print(df_transformed)
            loader_strategy.load(
                df=df_transformed
            )


class ETLLinkedinProfiles(ETL):
    """
    The role of this ETL is to get all data relatd to linkedin profiles
    """
    def extract(self):
        pass

    def transform(self):
        pass

    def load(self):
        pass
