import requests
import time
url = f"https://api.jikan.moe/v4/top/anime?page=1"
response = requests.get(url)
data = response.json()
liste_animes = data['data']

# On prend le premier animé de la liste (index 0)
premier_anime = liste_animes[0]

# On affiche ses clés pour voir les détails disponibles
print(premier_anime.keys())