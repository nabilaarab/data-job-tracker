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
        from etl.etl import ETLJobOffers
        etl_job_offers = ETLJobOffers()
        etl_job_offers.run_all()

    run()

etl_job_offers_pipeline()
