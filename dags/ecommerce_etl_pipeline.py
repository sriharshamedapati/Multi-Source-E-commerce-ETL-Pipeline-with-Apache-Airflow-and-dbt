from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import pandas as pd
import requests
import io
from datetime import datetime

def create_staging_schema():
    """Automates the creation of the staging schema before extraction."""
    hook = PostgresHook(postgres_conn_id='data_warehouse')
    hook.run("CREATE SCHEMA IF NOT EXISTS staging;")

def extract_api():
    all_orders = []
    page = 1
    while True:
        r = requests.get(f"http://mock_api:8000/orders?page={page}").json()
        if not r: break
        all_orders.extend(r)
        page += 1
    df = pd.DataFrame(all_orders)
    hook = PostgresHook(postgres_conn_id='data_warehouse')
    # FIXED: schema='staging', table_name='orders'
    df.to_sql('orders', hook.get_sqlalchemy_engine(), schema='staging', if_exists='replace', index=False)

def extract_s3():
    hook = S3Hook(aws_conn_id='aws_default')
    file_content = hook.read_key(key='inventory.csv', bucket_name='raw-data')
    df = pd.read_csv(io.StringIO(file_content))
    dw_hook = PostgresHook(postgres_conn_id='data_warehouse')
    # FIXED: schema='staging', table_name='inventory'
    df.to_sql('inventory', dw_hook.get_sqlalchemy_engine(), schema='staging', if_exists='replace', index=False)

def extract_db():
    src = PostgresHook(postgres_conn_id='source_db')
    dwh = PostgresHook(postgres_conn_id='data_warehouse')
    for t in ['users', 'products']:
        df = src.get_pandas_df(f"SELECT * FROM {t}")
        # FIXED: schema='staging', table_name matches {t}
        df.to_sql(t, dwh.get_sqlalchemy_engine(), schema='staging', if_exists='replace', index=False)

with DAG('ecommerce_etl_pipeline', start_date=datetime(2025,1,1), schedule='@daily', catchup=False) as dag:
    
    # NEW: Task to ensure the staging schema exists first
    setup_staging = PythonOperator(
        task_id='setup_staging',
        python_callable=create_staging_schema
    )

    e1 = PythonOperator(task_id='extract_api', python_callable=extract_api)
    e2 = PythonOperator(task_id='extract_s3', python_callable=extract_s3)
    e3 = PythonOperator(task_id='extract_db', python_callable=extract_db)

    # FIXED: Added --project-dir and used the simple dbt command
    dbt_run = BashOperator(
        task_id='dbt_run', 
        bash_command='cd /opt/airflow/dbt_project && dbt run --project-dir . --profiles-dir .'
    )
    
    dbt_test = BashOperator(
        task_id='dbt_test', 
        bash_command='cd /opt/airflow/dbt_project && dbt test --project-dir . --profiles-dir .'
    )

    setup_staging >> [e1, e2, e3] >> dbt_run >> dbt_test