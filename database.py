def zone_silver(dim_stats, fact_stats):
    #dim_stats.to_sql('dim_anime', conn, if_exists='replace', index=False)
    #fact_stats.to_sql('fact_anime', conn, if_exists='replace', index=False)
    dim_stats.write.mode("overwrite").format("delta").saveAsTable("data_anime_silver") 
    fact_stats.write.mode("overwrite").format("delta").saveAsTable("data_fact_silver")

def zone_bronze(df_anime):
    df_anime.write.mode("overwrite").format("delta").saveAsTable("data_anime_bronze") 
