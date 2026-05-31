import requests
import time

def extract_data(nb_pages):
    page = 1
    has_next_page = True
    animes_nettoyes = []
    

    while has_next_page and (page) <= (nb_pages):
        # On utilise les guillemets formatés (f"...") pour intégrer la variable page
        url = f"https://api.jikan.moe/v4/top/anime?page={page}"
        try :
                
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                liste_anime = data['data'] 
                animes_nettoyes.extend(liste_anime) 
                print(f"Page {page} récupérée avec succès !")
                has_next_page = data['pagination']['has_next_page']
                page += 1
                time.sleep(1)  # Pause pour respecter les limites de l'API
            else:
                print(f"Erreur lors de la récupération de la page {page}")
                break
        except requests.exceptions.RequestException as e:
            print(f"Erreur de connexion : {e}")
            break
    return animes_nettoyes
