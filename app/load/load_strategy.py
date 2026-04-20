import pandas as pd
from abc import ABC, abstractmethod

class LoadStrategy(ABC):
    """
    The responsability of this class is to load the data by using several method: Excel, Database, etc... 
    """
    @abstractmethod
    def load(df: pd.DataFrame, path_folder: str ="output/etl") -> bool:
        pass
