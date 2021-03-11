from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

import os

os.environ['SPARK_HOME'] = '/usr/local/hadoop-ecosystem/spark-3.0.2'
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.2,org.apache.spark:spark-streaming-kafka-0-10-assembly_2.12:3.0.2 pyspark-shell'


spark = SparkSession.builder.appName('Spark_Streaming').master('local[*]').enableHiveSupport().getOrCreate()

df = spark.readStream.format('kafka').option('kafka.bootstrap.servers','localhost:9092').option('subscribe','stationdata').option('startingOffsets','earliest').load()
df.printSchema()

df1 = df.selectExpr('CAST(value AS STRING)', 'timestamp')

schema = StructType().add('airTemperature',StringType()).add('gust',StringType()).add('humidity',StringType()).add('lat',StringType()).add('lng',StringType()).add('station_id',StringType()).add('time',StringType()).add('uvIndex',StringType()).add('windSpeed',StringType())

df2 = df1.select(from_json(col('value'),schema).alias('weather_detail'),'timestamp')

df3 = df2.select('weather_detail.*','timestamp')
df3.printSchema()

# df4 = df3.groupBy('station_id').agg({'airTemperature':'avg'}).select('station_id',col('avg(airTemperature)')).alias('avg_airTemperature')

# df_write_stream = df3.writeStream.trigger(processingTime='5 seconds').outputMode('append').option('truncate','false').format('hive').toTable('streamdb.weather_detail')

df_write_stream = df3.writeStream.trigger(processingTime='5 seconds').outputMode('append').option('truncate','false').format('parquet').option('checkpointLocation', '/capstone/checkpoint').option('path','/capstone/stream').start()

df_write_stream.awaitTermination()