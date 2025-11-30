from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "rafael",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="mxkeys_price_monitor",
    description="Monitoramento de preços Logitech MX Keys",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval="0 */4 * * *",  # a cada 4 horas
    catchup=False,
    tags=["scraping", "mxkeys"]
) as dag:

    scraper_task = BashOperator(
        task_id="run_scraper",
        bash_command="cd /opt && python -m scraper.main"
    )
