import sqlite3
import pandas as pd

conn = sqlite3.connect('animes.db')
df_test = pd.read_sql_query("" \
"SELECT categorie, ROUND(AVG(episodes)) as Moyenne_episodes, COUNT(episodes) as Nombre_animes FROM top_animes GROUP BY categorie ORDER BY Nombre_animes DESC", conn)
print(df_test)
conn.close()