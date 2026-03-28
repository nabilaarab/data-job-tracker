from abc import ABC, abstractmethod

class ETLAdapter(ABC):
    """
    This class allows to use the design pattern Adapter.
    It makes easy to use some library or API for ETL classes
    """
    @abstractmethod
    def request():
        pass


class ETLAdapterLibraryJobSpy(ETLAdapter):
    """
    This class makes Easy to use the Library JobSpy and then get job offers from Linkedin or Indeed.
    """

    def request():
        pass


class ETLAdapterAPIJobCloud():
    """
    This class makes easy to use the API of the company JobCloud which can get data from Jobs.ch or Jobup.ch
    """
