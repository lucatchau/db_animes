import logging
import argparse
import sys
from extract import extract_data
from transform import transform_save
from database import save_to_database
import os

os.environ['HADOOP_HOME'] = r'C:\Users\berger\Downloads\test\hadoop'

logging.basicConfig(
    level=logging.INFO,
      format="%(asctime)s - %(levelname)s - %(message)s",
      datefmt='%Y-%m-%d %H:%M:%S',
      handlers=[
          logging.FileHandler("pipeline_exec.log", encoding='utf-8'),
          logging.StreamHandler()
      ]
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--pages', type=int, default=2, help='Nombre de pages à extraire (20 animes par page)')
    args = parser.parse_args()
    liste_brute = extract_data(args.pages)
    logging.info(f"{len(liste_brute)} animes extraits.")
    if not liste_brute:
        sys.exit("Aucune donnée extraite. Veuillez vérifier votre connexion ou les paramètres de l'API.")
    fact_stats, dim_anime = transform_save(liste_brute)
    logging.info("Données transformées.")
    save_to_database(fact_stats, dim_anime)
    logging.info("Données sauvegardées au format Parquet.")
    logging.info("Processus terminé avec succès !")