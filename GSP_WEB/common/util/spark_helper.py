from pyspark import SparkConf, SQLContext
from pyspark.sql import SparkSession

def getSqlContext(index, table, tempviewname):
    conf = SparkConf()
    jar_path = "/usr/gsp/lib/spark/jars/elasticsearch-spark-20_2.11-5.6.4.jar"
    spark = SparkSession.builder.master("spark://localhost:7077").appName('gsp_web') \
        .config("spark.dynamicAllocation.enabled", "true") \
        .config("spark.shuffle.service.enabled", "true") \
        .config("spark.debug.maxToStringFields", 35) \
        .config("spark.jars", jar_path).config("es.nodes", "localhost:9200").getOrCreate()

    sqlContext = SQLContext(spark.sparkContext)

    target = index + "/" + table

    df = sqlContext.read.option("es.resource", target).format("org.elasticsearch.spark.sql").load()
    df.createOrReplaceTempView(tempviewname)

    return sqlContext

def getSqlContext_DF(index, table, tempviewname):
    conf = SparkConf()
    jar_path = "/usr/gsp/lib/spark/jars/elasticsearch-spark-20_2.11-5.6.4.jar"
    spark = SparkSession.builder.master("spark://localhost:7077").appName('gsp_web') \
        .config("spark.sql.tungsten.enabled", "true") \
        .config("spark.io.compression.codec", "snappy") \
        .config("spark.rdd.compress", "true") \
        .config("spark.streaming.backpressure.enabled", "true") \
        .config("spark.sql.parquet.compression.codec", "snappy") \
        .config("spark.jars", jar_path).config("es.nodes", "localhost:9200").getOrCreate()

    sqlContext = SQLContext(spark.sparkContext)

    target = index + "/" + table

    df = sqlContext.read.option("es.resource", target).format("org.elasticsearch.spark.sql").load()
    df.createOrReplaceTempView(tempviewname)

    return df