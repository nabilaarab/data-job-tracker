from abc import ABC, abstractmethod

class ETL(ABC):
    """
    It is an abstract class which explain the behavior of an ETL.
    """
    @abstractmethod
    def extract():
        pass

    @abstractmethod
    def transform():
        pass

    @abstractmethod
    def load():
        pass

    def run_all(self):
        """
        run extract then transform then load.
        """
        self.extract()
        self.transform()
        self.load()


class ETLJobOffers(ETL):
    """
    The role of this ETL is to get all data related of job offers.
    """
    def extract():
        pass

    def transform():
        pass

    def load():
        pass


class ETLLinkedinProfiles(ETL):
    """
    The role of this ETL is to get all data relatd to linkedin profiles
    """
    def extract():
        pass

    def transform():
        pass

    def load():
        pass
