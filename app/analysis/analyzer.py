from abc import ABC, abstractmethod


class Analyzer(ABC):
    @abstractmethod
    def run(self):
        """
        Launch the analyze by the strategy chose.
        """
        pass
