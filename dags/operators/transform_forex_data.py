# from pyspark.sql import SparkSession

def transform_forex_data(ti):
    file_path = ti.xcom_pull(task_ids='pull_forex_data')
    print(file_path)
    # spark = SparkSession.builder.appName('feature-engineering').getOrCreate()
    
    # df = spark.read.csv(file_path, header=True, inferSchema=True)
    # print(df)

    # as far as I know I need to have the docker image built first so that
    # by having a dockerfile indicating that the requirements.txt file must be
    # installed in the container so I can use packages like java, jdk, pyspark
    # pandas and any other python package