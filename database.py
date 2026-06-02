def save_to_database(dim_stats, fact_stats):
    #dim_stats.to_sql('dim_anime', conn, if_exists='replace', index=False)
    #fact_stats.to_sql('fact_anime', conn, if_exists='replace', index=False)
    dim_stats.write.mode("overwrite").format("delta").save("data_anime_delta") 
    fact_stats.write.mode("overwrite").format("delta").save("data_fact_delta")

def zone_bronze(df_anime):
    df_anime.write.mode("overwrite").format("delta").save("data_anime_delta") 
