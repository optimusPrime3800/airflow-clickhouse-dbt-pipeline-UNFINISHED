from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime


with DAG(
    dag_id="analytics_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["clickhouse", "dbt"],
) as dag:

    generate_data = BashOperator(
        task_id="generate_data",
        bash_command=(
            "python /opt/airflow/scripts/generate_data.py"
        ),
    )

    load_to_clickhouse = BashOperator(
        task_id="load_to_clickhouse",
        bash_command=(
            "python /opt/airflow/scripts/load_to_clickhouse.py"
        ),
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=(
            "cd /opt/airflow/dbt && "
            "dbt run "
            "--project-dir /opt/airflow/dbt "
            "--profiles-dir /opt/airflow/dbt"
        ),
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=(
            "cd /opt/airflow/dbt && "
            "dbt test "
            "--project-dir /opt/airflow/dbt "
            "--profiles-dir /opt/airflow/dbt"
        ),
    )

    generate_data >> load_to_clickhouse >> dbt_run >> dbt_test