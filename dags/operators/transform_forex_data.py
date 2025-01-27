from pyspark.sql import SparkSession
import sys

def transform_forex_data(file_path):
    print(f"CSV FILE PATH: {file_path}")
    spark = SparkSession.builder.appName('feature-engineering').getOrCreate()

    usd_php_forex_4h_spark_df = spark.read.csv(file_path, header=True, inferSchema=True)
    usd_php_forex_4h_spark_df.createOrReplaceTempView("usd_php_forex")
    result = spark.sql("""
        SELECT 
            v AS volume, 
            vw AS volume_weighted, 
            o AS opening_price,
            c AS closing_price,
            h AS highest_price,
            l AS lowest_price,
            t AS timestamp,
            n AS transactions,
            CAST(FROM_UNIXTIME(t / 1000) AS TIMESTAMP) AS new_datetime 
        FROM usd_php_forex;
    """)
    result.show()

    # as far as I know I need to have the docker image built first so that
    # by having a dockerfile indicating that the requirements.txt file must be
    # installed in the container so I can use packages like java, jdk, pyspark
    # pandas and any other python package

if __name__ == "__main__":
    # access argument vectors given in spark submit job operator
    # which will be the path to the newly saved .csv file
    file_path = sys.argv[1]

    # pass file path to task
    transform_forex_data(file_path=file_path)