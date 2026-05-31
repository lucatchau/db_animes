import requests
import pandas as pd
import time
import argparse
import sqlite3
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
    
def extraire_données(nb_pages):
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



def transform_save(liste_donnees_brute, conn):
    animes_nettoyes = []
    for anime in liste_donnees_brute:
                # On harmonise les clés : tout en minuscules, sans espaces ni symboles
                donnees_anime = {
                    'title_english': anime['title_english'],
                    'type': anime['type'],
                    'episodes': anime['episodes'],
                    'rank': anime['rank']
                }
                animes_nettoyes.append(donnees_anime)
            

    # Création du DataFrame
    df_animes = pd.DataFrame(animes_nettoyes)

    # Nettoyage et conversion (tout en minuscules pour correspondre aux clés ci-dessus)
    df_animes['episodes'] = df_animes['episodes'].fillna(0).astype(int)
    df_animes['title_english'] = df_animes['title_english'].fillna('Inconnu')

    df_animes['categorie'] = df_animes['type'].apply(categoriser_anime)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM top_animes")
    # Sauvegarde
    df_animes.to_sql('top_animes', conn, if_exists='append', index=False)
    conn.commit()
    print(f"Extraction réussie ! Fichier sauvegardé avec {len(df_animes)} lignes.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pages', type=int, default=2, help='Nombre de pages à extraire (20 animes par page)')
    args = parser.parse_args()
    conn = sqlite3.connect('animes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS top_animes (
            title_english TEXT,
            type TEXT,
            episodes INTEGER,
            rank INTEGER PRIMARY KEY,
            categorie TEXT
        )
    ''')
    liste_brute = extraire_données(args.pages)
    transform_save(liste_brute, conn)
    conn.commit()
    conn.close()

