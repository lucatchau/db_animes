import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, round

# 2. On démarre notre session Spark
spark = SparkSession.builder \
    .appName("AnimeAnalytics") \
    .getOrCreate()

# 3. On charge nos dossiers Parquet
print("Chargement des données Parquet...")
df_anime = spark.read.table("data_anime_silver")
df_fact = spark.read.table("data_fact_silver")


# 4. On inspecte ce qu'il y a dedans
print("\n--- Structure de la table Dimension Anime ---")
df_anime.printSchema()

print("\n--- Structure de la table des Faits ---")
df_fact.printSchema()
