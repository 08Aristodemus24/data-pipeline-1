import sys
import datetime as dt
import os
import shutil
import time

from pathlib import Path

from airflow import DAG, settings
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.models import Variable, Connection 
from airflow.configuration import conf
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

from utilities.preprocessors import reformat_date
from operators.pull_forex_data import pull_forex_data
from operators.test_pull_forex_data import test_pull_forex_data
from operators.transform_forex_data import transform_forex_data

from airflow.providers.amazon.aws.operators.s3 import S3CreateBucketOperator
from airflow.providers.amazon.aws.transfers.local_to_s3 import (
    LocalFilesystemToS3Operator,
)
from airflow.providers.amazon.aws.transfers.sql_to_s3 import SqlToS3Operator


# go to this site if you want to use cron instead of datetime to set schedule_interval
# https://crontab.guru/#00_12_*_*_Sun



def get_env_vars(ti):
    """
    push api key to xcom so that pull_forex_data can access
    this xcom    
    """
    api_key = Variable.get("POLYGON_API_KEY")
    aws_s3_region_name = Variable.get("AWS_S3_REGION_NAME")

    print(type(aws_s3_region_name))
    ti.xcom_push(key="api_key", value=api_key)
    ti.xcom_push(key="aws_s3_region_name", value=aws_s3_region_name)

# get airflow folder
airflow_home = conf.get('core', 'dags_folder')

# base dir would be /usr/local/airflow/
BASE_DIR = Path(airflow_home).resolve().parent

# data dir once joined with base dir would be /usr/local/airflow/include/data/
DATA_DIR = os.path.join(BASE_DIR, 'include/data')

# bucket name
BUCKET_NAME = "usd-php-ml-pipeline-bucket"

default_args = {
    'owner': 'mikhail',
    'retries': 3,
    'retry_delay': dt.timedelta(minutes=2)
}

with DAG(
    dag_id="forex_ml_pipeline",
    default_args=default_args,
    description="pull forex of usd to php data from last january 1 2024 up to january 2025 in intervals of 4 hours",
    start_date=dt.datetime(2024, 1, 1, 12),

    # runs every sunday at 12:00 
    schedule_interval="00 12 * * Sun",
    catchup=False
) as dag:
    
    get_env_vars_task = PythonOperator(
        task_id="get_env_vars",
        python_callable=get_env_vars
    )

    create_s3_bucket_task = S3CreateBucketOperator(
        task_id="create_s3_bucket",
        aws_conn_id="my_s3_conn",
        bucket_name=BUCKET_NAME, 
        # region_name="{{ti.xcom_pull(key='aws_s3_region_name', task_ids='get_env_vars')}}"
        region_name="us-east-2"
    )
    
    pull_forex_data_task = PythonOperator(
        task_id='pull_forex_data',
        python_callable=test_pull_forex_data,
        # python_callable=pull_forex_data,
        op_kwargs={
            # "start_date": "january 1 2024",
            # "end_date": "january 1 2025",
            # "ticker": "C:USDPHP",
            # "multiplier": 4,
            # "timespan": "hour",
            "formatter": reformat_date,
            "save_path": DATA_DIR
        }
    )
    
    transform_forex_data_task = SparkSubmitOperator(
        task_id='transform_forex_data',
        conn_id='my_spark_conn',
        application='./dags/operators/transform_forex_data.py',

        # pass argument vector to spark submit job operator since
        # it is a file that runs like a script
        application_args=["{{ti.xcom_pull(key='new_file_path', task_ids='test_pull_forex_data')}}"],
        # application_args=["{{ti.xcom_pull(key='file_path', task_ids='pull_forex_data')}}"],
        verbose=True
    )
    
    get_env_vars_task >> create_s3_bucket_task >> pull_forex_data_task >> transform_forex_data_task