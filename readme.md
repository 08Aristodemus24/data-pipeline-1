# This is my first data engineering project aiming to create data pipeline to extract eeg signals, transform them into usable features, and load the tables into a data warehouse.

# Usage:
1. clone repository with `git clone https://github.com/08Aristodemus24/eeg-ml-pipeline`
2. navigate to directory with `readme.md` and `requirements.txt` file
3. run command; `conda create -n <name of env e.g. eeg-ml-pipeline> python=3.12.3`. Note that 3.12.3 must be the python version otherwise packages to be installed would not be compatible with a different python version
4. once environment is created activate it by running command `conda activate`
5. then run `conda activate eeg-ml-pipeline`
6. check if pip is installed by running `conda list -e` and checking list
7. if it is there then move to step 8, if not then install `pip` by typing `conda install pip`
8. if `pip` exists or install is done run `pip install -r requirements.txt` in the directory you are currently in

# Tools that I might use:
* Apache Airflow - data orchestration, workflow, and manager for steps in the data pipeline
* Snowflake/Databricks - for data warehousing
* Apache Spark (PySpark)/DBT (data build tool) - for transforming the raw eeg signals into usable features
* Amazon S3 - store raw eeg, and the transformed features

# Articles, Videos, Research Papers:
* building a data pipeline using airflow, apache spark, emr, & snowflake: https://youtu.be/hK4kPvJawv8?si=4n4rkcgdzB26fasQ
* free tools used for data engineering projects: https://www.youtube.com/watch?v=M7eGUM28Ke4&list=PLCBT00GZN_SAzwTS-SuLRM547_4MUHPuM&index=28&pp=gAQBiAQB
* https://stackoverflow.com/questions/47811129/requests-in-python-is-not-downloading-file-completely
* https://realpython.com/python-download-file-from-url/
* 

# Data sources:
* motor imagery eeg: http://gigadb.org/dataset/100295
* database for ecg signals: https://physionet.org/about/database/
* healthcare data api: https://data.cms.gov/provider-data/search
* kaggle eeg features: https://www.kaggle.com/code/huvinh/eeg-extract-features
* book api: 
https://openlibrary.org/dev/docs/api/books
https://openlibrary.org/developers/api