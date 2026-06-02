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
df_anime = spark.read.parquet("data_anime_parquet")
df_fact = spark.read.parquet("data_fact_parquet")
df_anime.createOrReplaceTempView("view_anime")
df_fact.createOrReplaceTempView("view_fact")


# 4. On inspecte ce qu'il y a dedans
print("\n--- Structure de la table Dimension Anime ---")
df_anime.printSchema()

print("\n--- Structure de la table des Faits ---")
df_fact.printSchema()
pd = """
WITH table_classement AS (
    SELECT 
        f.title_english,
        f.rating,
        a.favorites,
        RANK() OVER(PARTITION BY f.rating ORDER BY a.favorites DESC) AS rang
    FROM view_anime a
    JOIN view_fact f ON a.mal_id = f.mal_id
)
SELECT * FROM table_classement 
WHERE rang <= 2
ORDER BY rating, rang
"""
# On affiche un aperçu des 5 premières lignes
df_resultat_sql = spark.sql(pd)
df_resultat_sql.show(20)