import sqlite3
import argparse
import sys
from extract import extract_data
from transform import transform_save
from database import initiate_database
from database import save_to_database

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--pages', type=int, default=2, help='Nombre de pages à extraire (20 animes par page)')
    args = parser.parse_args()
    conn = sqlite3.connect('animes.db')
    initiate_database(conn)
    print("Base de données initialisée.")
    liste_brute = extract_data(args.pages)
    print(f"{len(liste_brute)} animes extraits.")
    if not liste_brute:
        sys.exit("Aucune donnée extraite. Veuillez vérifier votre connexion ou les paramètres de l'API.")
    fact_stats, dim_anime = transform_save(liste_brute, conn)
    print("Données transformées.")
    save_to_database(fact_stats, dim_anime)
    print("Données sauvegardées dans la base de données.")
    conn.commit()
    conn.close()
    print("Processus terminé avec succès !")