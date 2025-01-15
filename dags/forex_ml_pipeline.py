import sys
import datetime as dt
import os
import shutil
import time

from pathlib import Path
from dotenv import load_dotenv

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from airflow.configuration import conf

from utilities.preprocessors import reformat_date
from operators.pull_forex_data import pull_forex_data
from operators.transform_forex_data import transform_forex_data
# # pip install 'apache-airflow[amazon]'
# from airflow.providers.amazon.aws.operators.s3 import S3CreateBucketOperator
# from airflow.providers.amazon.aws.transfers.local_to_s3 import (
#     LocalFilesystemToS3Operator,
# )
# from airflow.providers.amazon.aws.transfers.sql_to_s3 import SqlToS3Operator


# go to this site if you want to use cron instead of datetime to set schedule_interval
# https://crontab.guru/#00_12_*_*_Sun


def test_pull_forex_data():
    return "/opt/***/data/usd_php_forex_4hour.csv"

# POLYGON_API_KEY = os.environ.get('POLYGON_API_KEY')
POLYGON_API_KEY = Variable.get('POLYGON_API_KEY')

airflow_home = conf.get('core', 'dags_folder')
BASE_DIR = Path(airflow_home).resolve().parent
DATA_DIR = os.path.join(BASE_DIR, 'data')

default_args = {
    'owner': 'mikhail',
    'retries': 5,
    'retry_delay': dt.timedelta(minutes=2)
}

with DAG(
    dag_id="forex_ml_pipeline",
    default_args=default_args,
    description="pull forex of usd to php data from last january 1 2024 up to january 2025 in intervals of 4 hours",
    start_date=dt.datetime(2024, 1, 1, 12),

    # runs every sunday at 12:00 
    schedule_interval="00 12 * * Sun",
    catchup=True
) as dag:
    
    # pull_forex_data = PythonOperator(
    #     task_id='pull_forex_data',
    #     python_callable=pull_forex_data,
    #     op_kwargs={
    #         "formatter": reformat_date,
    #         "api_key": POLYGON_API_KEY,
    #         "save_path": DATA_DIR
    #     }
    # )

    pull_forex_data = PythonOperator(
        task_id='pull_forex_data',
        python_callable=test_pull_forex_data,
    )

    transform_forex_data = PythonOperator(
        task_id='transform_forex_data',
        python_callable=transform_forex_data
    )

    pull_forex_data >> transform_forex_data