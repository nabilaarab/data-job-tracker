import pandas as pd
from etl.utils import load_config
from etl.etl import ETL
from etl.extract.extract_adapter_api_job_cloud import ExtractAdapterAPIJobCloud
from etl.extract.extract_adapter_library_jobspy import ExtractAdapterLibraryJobSpy

class ETLJobOffers(ETL):
    """
    The role of this ETL is to get all data related of job offers.
    """
    def __init__(self, config=None):
        super().__init__()
        self.extractors = [
            ExtractAdapterLibraryJobSpy,
            ExtractAdapterAPIJobCloud
            ]

        if config is None:
            self.config = load_config()


    def extract(self):
        """
        """
        data = {}
        for extract_method in self.extractors:
            results = []
            for location in self.config.locations:
                for key_word in self.config.key_words:
                    print(f"Search {key_word} in {location}")

                    jobs = extract_method.request(self.config, location, key_word)
                    jobs = extract_method.to_dataframe(jobs)

                    results.append(jobs)
                    
            data[extract_method.__class__] = pd.concat(results, ignore_index=True)

        return data
    

    def transform(self, data_extracted: dict):
        """
        """
        # Data treatment from JoSpy library
        data_jobspy = data_extracted.get(ExtractAdapterLibraryJobSpy)
        if data_jobspy is not None:
            pass
        
        # Data treatment from JobCloud APIs
        data_jobcloud = data_extracted.get(ExtractAdapterAPIJobCloud)
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
