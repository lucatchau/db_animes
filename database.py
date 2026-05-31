def save_to_database(dim_stats, fact_stats):
    #dim_stats.to_sql('dim_anime', conn, if_exists='replace', index=False)
    #fact_stats.to_sql('fact_anime', conn, if_exists='replace', index=False)
    dim_stats.write.mode("overwrite").parquet("data_anime_parquet") 
    fact_stats.write.mode("overwrite").parquet("data_fact_parquet")