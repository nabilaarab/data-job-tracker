from airflow.decorators import dag, task
from datetime import datetime

@dag(
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    is_paused_upon_creation=False
)
def etl_job_offers_pipeline():
    
    @task
    def run():
        from pipeline.pipeline import PipelineJobOffer
        PipelineJobOffer.run()

    run()

etl_job_offers_pipeline()
