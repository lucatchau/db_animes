import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, round, explode, col, sum
from database import zone_gold


# 2. On démarre notre session Spark
spark = SparkSession.builder \
    .appName("AnimeAnalytics") \
    .getOrCreate()

# 3. On charge nos dossiers Parquet
print("Chargement des données Parquet...")
df_anime = spark.read.table("data_anime_silver")
df_fact = spark.read.table("data_fact_silver")
df_anime.createOrReplaceTempView("view_anime")
df_fact.createOrReplaceTempView("view_fact")

df_combined = df_anime.join(df_fact, on='mal_id', how='inner')
df_exploded = df_combined.withColumn("studio_name", explode(col("studio_name")))
df_moyenne = df_exploded.groupBy("studio_name").agg(
    round(avg("score"), 2).alias("moyenne_score"),
    sum(col("favorites")).alias("Total favoris")
    )

zone_gold(df_moyenne)
print("\n--- Structure de la table des Faits ---")
df_moyenne.printSchema()

