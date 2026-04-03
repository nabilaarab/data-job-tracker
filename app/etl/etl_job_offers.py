import pandas as pd
from etl.utils import load_config
from etl.etl import ETL
from etl.extract.utils import html_to_text
from etl.extract.extract_adapter import ExtractAdapter
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

    # function: extract --------------------------------------------------------------------------------------
    def extract(self):
        """
        """
        data = {}
        for extract_method in self.extractors:
            extract_method: ExtractAdapter
            res = extract_method.request(self.config)

            data[extract_method] = res

        return data
    
    # function: transform ------------------------------------------------------------------------------------
    def transform(self, data_extracted: dict):
        """
        """
        data = []
        for extractor in self.extractors:
            extractor: ExtractAdapter
            data_to_transform = data_extracted.get(extractor)
            print("ici")
            print(type(data_to_transform))
            print(len(data_to_transform))
            print(data_to_transform)
            # IF THE SOURCE IS THE JOBSPY LIBRARY
            if extractor == ExtractAdapterLibraryJobSpy:
                data_to_transform = pd.concat(data_to_transform, ignore_index=True)
            
            # IF THE SOURCE IS THE JOBCLOUD API
            print(ExtractAdapterAPIJobCloud)
            print(extractor)
            if extractor == ExtractAdapterAPIJobCloud:
                dfs = []
                for i in range(0, len(data_to_transform)):
                    df = self.__to_dataframe_reply_api_jobcloud(data_to_transform[i])
                    dfs.append(df)

                data_to_transform = pd.concat(dfs, ignore_index=True)

            data.append(data_to_transform)
            
        return pd.concat(data, ignore_index=True)

    # function: load ------------------------------------------------------------------------------------------
    def load(self, df_transformed: pd.DataFrame):
        """
        """
        for loader_strategy in self.loader_strategies:
            print(type(df_transformed))
            print(df_transformed)
            loader_strategy.load(
                df=df_transformed
            )

    # function: to_dataframe ------------------------------------------------------------------------
    # WARNING : split this functions ! Too much responsability
    @staticmethod
    def __to_dataframe_reply_api_jobcloud(data) -> pd.DataFrame:
        """This function get the result of the request and transform it in DataFrame

        Args:
            data (_type_): _description_

        Returns:
            pd.DataFrame: _description_
        """
        # CONVERT TO DATAFRAME
        dfs = []
        for website in data:
            data_website_selected =  data[website]

            df_website_selected = pd.DataFrame(data_website_selected)
            df_website_selected["site"] = website

            dfs.append(df_website_selected)

        df_merged: pd.DataFrame = pd.concat(dfs)


        # GET LOCATIONS
        from_series_jobs_locations = df_merged["locations"].tolist()
        
        jobs_locations = []
        for from_series_job_locations in from_series_jobs_locations:
            job_locations = []
            str_locations = ""
            for dict_location in from_series_job_locations:
                for key in dict_location:
                    str_locations += str(dict_location[key]) + " "
                job_locations.append(str_locations)

            jobs_locations.append(job_locations)

        #print(jobs_locations)

        # GET URL
        _links_list = df_merged["_links"].tolist()

        urls = []
        detail_languages = ["detail_fr", "detail_en", "detail_de"]

        for _links in _links_list:
            for detail_language in detail_languages:
                if detail_language in _links:
                    urls.append(_links[detail_language]["href"])
                    break
        
        
        # RENAME COLUMNS
        df_final = pd.DataFrame(
            {
                "id": df_merged["job_id"],
                "site": df_merged["site"],
                "job_url": urls,
                "title": df_merged["title"],
                "description": df_merged["template_text"].apply(html_to_text),
                "job_url_direct": df_merged["external_url"],
                "company": df_merged["company_name"],
                "location": jobs_locations,
                "date_posted": df_merged["last_online_date"],
                "contacts": df_merged["contacts"],
            }
        )


        return df_final
