import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, BooleanType, FloatType, ArrayType
from pyspark.sql.functions import when, col

schema_entite = StructType([
    StructField("mal_id", IntegerType(), True),
    StructField("name", StringType(), True)
])


# Définition du schéma pour le DataFrame
schema = StructType([
    StructField("mal_id", IntegerType(), True),
    StructField("title_english", StringType(), True),
    StructField("type", StringType(), True),
    StructField("episodes", IntegerType(), True),
    StructField("rank", IntegerType(), True),
    StructField("score", FloatType(), True),
    StructField("favorites", IntegerType(), True),
    StructField("airing", BooleanType(), True),
    StructField("rating", StringType(), True),
    StructField("studios", ArrayType(schema_entite), True),
    StructField("producers", ArrayType(schema_entite), True)

])

def categoriser_anime(type_brut):
    try :
            type_propre = type_brut.strip().upper()  # On nettoie et met en majuscules pour uniformiser
            if type_propre == 'TV':
                return 'Série'
            elif type_propre == 'OVA':
                return 'OAV'
            else:
                return 'Autre'
    except:
        return 'Autre'
        

def transform_save(liste_donnees_brute):
    spark = SparkSession.builder \
    .master("local") \
    .appName("Projet Anime") \
    .getOrCreate()
    # Création du DataFrame
    df_animes = spark.createDataFrame(liste_donnees_brute, schema=schema)
    # METHODE PANDAS : fact_stats = df_animes[['mal_id', 'episodes', 'rank', 'score', 'favorites']] 

    fact_stats = df_animes.select('mal_id', 'episodes', 'rank', 'score', 'favorites') # METHODE SPARK 
    dim_anime = df_animes.select('mal_id', 'title_english', 'type', 'airing', 'rating', 'studios', 'producers').dropDuplicates(subset=['mal_id'])  # METHODE SPARK 
    
    # METHODE PANDAS :dim_anime = dim_anime.drop_duplicates(subset=['mal_id'])  # On garde une seule entrée par anime

    # Nettoyage et conversion (tout en minuscules pour correspondre aux clés ci-dessus)
    df_animes = df_animes.fillna({'episodes': 0, 'title_english': 'Inconnu', 'rank': 0, 'score': 0.0, 'favorites': 0, 'airing': False, 'rating': 'Unknown'})
    df_animes = df_animes.withColumn(
        "categorie", 
        when(col("type") == "TV", "Série").when(col("type") == "OVA", "OAV").otherwise("Autre")
    )

    print(f"Extraction réussie")
    return fact_stats, dim_anime