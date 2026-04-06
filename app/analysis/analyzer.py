from abc import ABC, abstractmethod
from analysis.models import AnalyzerConfig

class Analyzer(ABC):
    def __init__(self, config: AnalyzerConfig):
        self._config = config

    @abstractmethod
    def run(self):
        """
        Launch the analyze by the strategy chose.
        """
        pass
