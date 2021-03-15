from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

import os

# Load pyspark arguements
os.environ['SPARK_HOME'] = '/usr/local/hadoop-ecosystem/spark-3.0.2'
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.2,org.apache.spark:spark-streaming-kafka-0-10-assembly_2.12:3.0.2 pyspark-shell'

# Create spark session
spark = SparkSession.builder.appName('Spark_Streaming').master('local[*]').enableHiveSupport().getOrCreate()

# Read 'latest' stream from 'datastation' topic
df = spark.readStream.format('kafka').option('kafka.bootstrap.servers','localhost:9092').option('subscribe','datastation').option('startingOffsets','latest').load()
df.printSchema()

# Parse values into string with timestamp
df1 = df.selectExpr('CAST(value AS STRING)', 'timestamp')

# Create then add schema to dataframe 
schema = StructType().add('airTemperature',StringType()).add('gust',StringType()).add('humidity',StringType()).add('lat',StringType()).add('lng',StringType()).add('station_id',StringType()).add('time',StringType()).add('uvIndex',StringType()).add('windSpeed',StringType())
df2 = df1.select(from_json(col('value'),schema).alias('weather_detail'),'timestamp')

# Select all relevant values with timestamp into df3
df3 = df2.select('weather_detail.*','timestamp')
df3.printSchema()

# Write checkpoint metadata in hdfs:/capstone/checkpoint
# Write actual data into partitioned parquet files in hdfs:/capstone/stream
df_write_stream = df3.writeStream.trigger(processingTime='5 seconds').outputMode('append').option('truncate','false').format('parquet').option('checkpointLocation', '/capstone/checkpoint').option('path','/capstone/stream').start()

df_write_stream.awaitTermination()