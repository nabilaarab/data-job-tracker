from abc import ABC, abstractmethod
from pipeline_step import PipelineStepJobAnalyzerKeyWords, PipelineStepJobAnalyzerLLM

class Pipeline(ABC):
    _steps = []

    @classmethod
    def run(cls):
        for step in cls._steps:
            step.run()


class PipelineJobOffer(Pipeline):
    """This class allows you to scrape the data, analyze and use them."""

    _steps = [
        PipelineStepJobAnalyzerKeyWords(),
        PipelineStepJobAnalyzerLLM()
    ]
