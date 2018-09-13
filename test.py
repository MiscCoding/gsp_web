from pyspark import SparkContext, SQLContext
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split

from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext

jar_path = "/usr/gsp/lib/spark/jars/elasticsearch-spark-20_2.11-5.6.4.jar"
spark = SparkSession.builder.master("spark://localhost:7077").appName('gsp_test')\
    .config("spark.sql.tungsten.enabled", "true")\
    .config("spark.io.compression.codec", "snappy")\
    .config("spark.rdd.compress", "true")\
    .config("spark.streaming.backpressure.enabled", "true")\
    .config("spark.sql.parquet.compression.codec", "snappy")\
    .config("spark.jars", jar_path).config("es.nodes", "192.168.10.134:9200").getOrCreate()
sqlContext = SQLContext(spark.sparkContext)

df = sqlContext.read.option("es.resource", "gsp-2018.01.10/ca_sip_dip").format("org.elasticsearch.spark.sql").load()
df.createOrReplaceTempView("tab")

sqlContext.sql("select * FROM tab ").collect()
sqlContext.sql("select * FROM tab ").show(1000)