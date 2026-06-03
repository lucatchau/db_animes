
df_combined = df_anime.join(df_fact, on='mal_id', how='inner')

df_moyenne = df_combined.groupBy("type").agg(round(avg("score"), 2).alias("moyenne_score"))
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
