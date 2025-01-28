from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import skewness, kurtosis, stddev
import sys

def transform_forex_data(file_path):
    print(f"CSV FILE PATH: {file_path}")
    spark = SparkSession.builder.appName('feature-engineering').getOrCreate()

    usd_php_forex_4h_spark_df = spark.read.csv(file_path, header=True, inferSchema=True)
    usd_php_forex_4h_spark_df.createOrReplaceTempView("usd_php_forex")

    # calculating moving average or mean of a window of 24 hours, 
    # because each row is 4 hours and 24 hours is basically 6 
    # samples of the data, we want to calculate the moving average
    # of 6 rows as it is 24 hours 
    result = spark.sql("""
        WITH trans_1 AS (SELECT 
            v AS volume, 
            vw AS volume_weighted, 
            o AS opening_price,
            c AS closing_price,
            h AS highest_price,
            l AS lowest_price,
            t AS timestamp,
            n AS transactions,
            CAST(FROM_UNIXTIME(t / 1000) AS TIMESTAMP) AS new_datetime 
        FROM usd_php_forex),

        trans_2 AS (SELECT
            *,
            MAX(closing_price) OVER(ORDER BY new_datetime ROWS BETWEEN 5 PRECEDING AND CURRENT ROW) AS moving_max_close,
            MIN(closing_price) OVER(ORDER BY new_datetime ROWS BETWEEN 5 PRECEDING AND CURRENT ROW) AS moving_min_close,
            AVG(closing_price) OVER(ORDER BY new_datetime ROWS BETWEEN 5 PRECEDING AND CURRENT ROW) AS moving_avg_close
        FROM trans_1),
                    
        trans_3 AS (SELECT
            *,
            (moving_max_close - moving_min_close) AS range_close
        FROM trans_2),
                    
        trans_4 AS (SELECT
            *,
            PERCENTILE(closing_price, 0.5) OVER(ORDER BY new_datetime ROWS BETWEEN 5 PRECEDING AND CURRENT ROW) AS moving_median_close   
        FROM trans_3)
                    
        SELECT * FROM trans_4;
    """)
    
    # ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW which would be a 7 day moving standard deviation
    window = Window.orderBy("new_datetime").rowsBetween(-5, Window.currentRow)

    final_features = result \
    .withColumn("moving_std_close", stddev("closing_price").over(window)) \
    .withColumn("moving_skew_close", skewness("closing_price").over(window)) \
    .withColumn("moving_kurt_close", kurtosis("closing_price").over(window))
    final_features.show()

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