from abc import ABC, abstractmethod
from pipeline.pipeline_step import PipelineStepInitContextJobOffers, PipelineStepExtractJobOffers, PipelineStepTransformJobOffers, PipelineStepLoadInExcel, PipelineStepJobAnalyzerKeyWords, PipelineStepJobAnalyzerLLM

class Pipeline(ABC):
    _steps = []

    @classmethod
    def run(cls):
        context = None
        for step in cls._steps:
            context = step.run(context)


class PipelineJobOffer(Pipeline):
    """This class allows you to scrape the data, analyze and use them."""

    _steps = [
        PipelineStepInitContextJobOffers(),
        PipelineStepExtractJobOffers(),
        PipelineStepTransformJobOffers(),
        PipelineStepLoadInExcel(),
        PipelineStepJobAnalyzerKeyWords(),
        PipelineStepLoadInExcel(),
        # PipelineStepJobAnalyzerLLM(),
        # PipelineStepLoadInExcel()
    ]
