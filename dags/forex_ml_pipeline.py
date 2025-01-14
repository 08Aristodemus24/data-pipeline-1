import sys
import datetime as dt
import os
import shutil
import time

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# pip install 'apache-airflow[amazon]'
# from airflow.providers.amazon.aws.operators.s3 import S3CreateBucketOperator
# from airflow.providers.amazon.aws.transfers.local_to_s3 import (
#     LocalFilesystemToS3Operator,
# )
# from airflow.providers.amazon.aws.transfers.sql_to_s3 import SqlToS3Operator


# go to this site if you want to use cron instead of datetime to set schedule_interval
# https://crontab.guru/#00_12_*_*_Sun

def test():
    print("hello world")

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
    
    pull_forex_data = PythonOperator(
        task_id='pull_forex_data',
        python_callable=test,
    )