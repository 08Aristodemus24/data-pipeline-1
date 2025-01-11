# This is my first data engineering project aiming to create data pipeline to extract eeg signals, transform them into usable features, and load the tables into a data warehouse.

# Usage:
1. clone repository with `git clone https://github.com/08Aristodemus24/data-pipeline-1`
2. navigate to directory with `readme.md` and `requirements.txt` file
3. run command; `conda create -n <name of env e.g. data-pipeline-1> python=3.12.3`. Note that 3.12.3 must be the python version otherwise packages to be installed would not be compatible with a different python version
4. once environment is created activate it by running command `conda activate`
5. then run `conda activate data-pipeline-1`
6. check if pip is installed by running `conda list -e` and checking list
7. if it is there then move to step 8, if not then install `pip` by typing `conda install pip`
8. if `pip` exists or install is done run `pip install -r requirements.txt` in the directory you are currently in
9. install jdk-17 and java 8 for apache spark
10. install airflow using this `pip install "apache-airflow[celery]==2.10.4" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.10.4/constraints-3.12.txt"`


# Tools that I might use:
* Apache Airflow - data orchestration, workflow, and manager for steps in the data pipeline
* Snowflake/Databricks - for data warehousing
* Apache Spark (PySpark)/DBT (data build tool) - for transforming the raw eeg signals into usable features
* Amazon S3 - store raw eeg, and the transformed features

# Resources:
## Videos:
* building a data pipeline using airflow, apache spark, emr, & snowflake: https://youtu.be/hK4kPvJawv8?si=4n4rkcgdzB26fasQ
* free tools used for data engineering projects: https://www.youtube.com/watch?v=M7eGUM28Ke4&list=PLCBT00GZN_SAzwTS-SuLRM547_4MUHPuM&index=28&pp=gAQBiAQB
* sql window functions: https://www.youtube.com/watch?v=7NBt0V8ebGk&list=PLCBT00GZN_SAzwTS-SuLRM547_4MUHPuM&index=2
## Articles:
* https://stackoverflow.com/questions/47811129/requests-in-python-is-not-downloading-file-completely
* https://realpython.com/python-download-file-from-url/
* pyspark and aws s3: https://medium.com/@bharadwajaryan30/handling-big-data-with-pyspark-and-aws-s3-f2a3f28419a9
* installing and configuring apache airflow: https://medium.com/orchestras-data-release-pipeline-blog/installing-and-configuring-apache-airflow-a-step-by-step-guide-5ff602c47a36
* 

# Data sources:
* motor imagery eeg: http://gigadb.org/dataset/100295
* database for ecg signals: https://physionet.org/about/database/
* healthcare data api: https://data.cms.gov/provider-data/search
* kaggle eeg features: https://www.kaggle.com/code/huvinh/eeg-extract-features
* book api: 
* https://openlibrary.org/dev/docs/api/books
* https://openlibrary.org/developers/api
* forex trades: https://polygon.io/docs/forex/getting-started
- keep an eye on forexTicker/currency pair since it has the attributes/columns you need for every time interval (e.g. day) such as closing price, opening price, highest price, lowest price, and volume all of which you can use for signal processing
* stock trades data: https://polygon.io/docs/stocks/
- keep an eye on tickers parameter since it represents the companys short name apple inc. for instance is short for AAPL and you can use this for the tickers parameter
* list of tickers in the stock market: https://stockanalysis.com/stocks/

we want ot get previous stocks from the last years let's say, and continue getting the stock or forex OHLC (open, high, low, close) for the coming days or depending what time interval you want

let's say we want to get the C:USDPHP