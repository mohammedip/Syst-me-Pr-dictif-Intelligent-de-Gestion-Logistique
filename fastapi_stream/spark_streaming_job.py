from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, IntegerType
from pyspark.ml import PipelineModel


spark = SparkSession.builder \
    .appName("LateDeliveryRiskStreaming") \
    .config("spark.sql.shuffle.partitions", "4") \
    .config("spark.streaming.stopGracefullyOnShutdown", "true") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")


schema = StructType() \
    .add("Type", StringType()) \
    .add("ProductCategoryId", IntegerType()) \
    .add("OrderItemQuantity", IntegerType()) \
    .add("CustomerCountry", StringType()) \
    .add("CustomerCity", StringType()) \
    .add("OrderCountry", StringType()) \
    .add("OrderCity", StringType()) \
    .add("ShippingMode", StringType()) \
    .add("order_month", IntegerType())



raw_stream = spark.readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", 9009) \
    .load()


json_stream = raw_stream.select(
    from_json(col("value"), schema).alias("data")
).select("data.*")


encoding_model = PipelineModel.load("../models/encoding_model")
encoded_stream = encoding_model.transform(json_stream)

clean_stream = encoded_stream.drop(
    "Type",
    "OrderCountry",
    "OrderCity",
    "ShippingMode",
    "CustomerCountry",
    "CustomerCity"
)


model_path = "../models/best_model"
pipeline_model = PipelineModel.load(model_path)



predictions = pipeline_model.transform(clean_stream)

output = predictions.select(
    "Type", "ProductCategoryId", "OrderItemQuantity",
    "CustomerCountry", "CustomerCity",
    "OrderCountry", "OrderCity",
    "ShippingMode", "order_month",
    "Late_delivery_risk"
)



postgres_url = "jdbc:postgresql://localhost:5432/dataco"
postgres_properties = {
    "user": "postgres",
    "password": "postgres",
    "driver": "org.postgresql.Driver"
}

query_pg = output.writeStream \
    .foreachBatch(
        lambda df, epochId:
            df.write.jdbc(
                url=postgres_url,
                table="late_delivery_stream",
                mode="append",
                properties=postgres_properties
            )
    ) \
    .outputMode("append") \
    .start()


query_mongo = output.writeStream \
    .format("mongo") \
    .option("uri", "mongodb://localhost:27017/dataco.late_delivery_stream") \
    .outputMode("append") \
    .start()



spark.streams.awaitAnyTermination()
