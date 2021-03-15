from pyspark.sql import SparkSession
from pymongo import MongoClient

import os

os.environ['SPARK_HOME'] = '/usr/local/hadoop-ecosystem/spark-3.0.2'

# Create spark session
spark = SparkSession.builder.appName('Hive_Spark_DF').master('local[*]').enableHiveSupport().getOrCreate()

# Merge all parquet files in hdfs:/capstone/stream into dataframe
parquet_df = spark.read.format('parquet').option('inferSchema','true').option('header','false').load('/capstone/stream/part-00000-*.snappy.parquet')

print(parquet_df.count())
parquet_df.show()

# Parse data into dictionaries (json-readable for MongoDB)
list_stations = map(lambda row: row.asDict(), parquet_df.collect())

# Connect with MondgoDB Atlas
client = MongoClient("mongodb+srv://tpacba:OneYear_95@cluster0.ufwrg.mongodb.net/station_data?retryWrites=true&w=majority")
db = client.station_data
collection = db.list_stations
print('Connected to MongoDB!')

# Upload each record into station_data.list_stations
for s in list_stations:
    collection.insert_one(s)
    print('{} inserted into {}'.format(s,collection))