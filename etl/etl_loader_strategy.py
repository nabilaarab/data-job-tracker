from abc import ABC, abstractmethod

class ETLLoaderStrategy(ABC):
    """
    The responsability of this class is to load the data by using several method: Excel, Database, etc... 
    """

    @abstractmethod
    def load() -> bool:
        """
        """
        pass


class ETLLoaderStrategyDatabase(ETLLoaderStrategy):
    """
    The responsability of this class is to load data in a database
    """
    def load():
        pass


class ETLLoaderStrategyExcel(ETLLoaderStrategy):
    """
    The responsability of this class is to load data in an excel
    """
    def load():
        pass
