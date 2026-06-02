import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, round

# 1. On force la variable d'environnement pour Windows
os.environ['HADOOP_HOME'] = r'C:\Users\Lucat\Downloads\test\hadoop'

# 2. On démarre notre session Spark
spark = SparkSession.builder \
    .appName("AnimeAnalytics") \
    .getOrCreate()



# 3. On charge nos dossiers Parquet
print("Chargement des données Parquet...")
df_anime = spark.read.format("delta").load("data_anime_delta")
df_fact = spark.read.format("delta").load("data_fact_delta")
df_anime.createOrReplaceTempView("view_anime")
df_fact.createOrReplaceTempView("view_fact")


df_combined = df_anime.join(df_fact, on='mal_id', how='inner')

df_moyenne = df_combined.groupBy("type").agg(round(avg("score"), 2).alias("moyenne_score"))
# 4. On inspecte ce qu'il y a dedans
print("\n--- Structure de la table Dimension Anime ---")
df_anime.printSchema()

print("\n--- Structure de la table des Faits ---")
df_fact.printSchema()
pd = """
SELECT
    type,
    ROUND(AVG(score), 2) AS moyenne_score
    FROM view_anime a
    JOIN view_fact f ON a.mal_id = f.mal_id
    GROUP BY type
    ORDER BY moyenne_score DESC
"""
# On affiche un aperçu des 5 premières lignes
df_moyenne.sort("moyenne_score", ascending=False).show(5)