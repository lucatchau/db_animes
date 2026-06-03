import logging
import sys
from extract import extract_data
from transform import transform_save
from database import zone_silver  # Aligné avec notre nouveau database.py
from pyspark.sql import SparkSession

# Configuration des logs : On garde UNIQUEMENT la console (Stream), Databricks gère le reste
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.StreamHandler()]
)

if __name__ == "__main__":
    logging.info("Démarrage du pipeline d'animes...")

    # 1. Gestion des paramètres version Databricks (Widgets)
    # Crée un champ de texte en haut de l'écran. Par défaut : 2 pages.
    dbutils.widgets.text("pages", "2", "Nombre de pages à extraire")
    
    # Récupération de la valeur entrée par l'utilisateur ou l'orchestrateur
    nb_pages = int(dbutils.widgets.get("pages"))
    
    # 2. EXTRACTION
    logging.info(f"Lancement de l'extraction de l'API (Pages demandées : {nb_pages})...")
    liste_brute = extract_data(nb_pages)
    logging.info(f"{len(liste_brute)} animes extraits du site Jikan.")
    
    if not liste_brute:
        logging.error("Aucune donnée extraite. Arrêt du pipeline.")
        sys.exit("Aucune donnée extraite. Veuillez vérifier votre connexion ou les paramètres de l'API.")
        
    # 3. TRANSFORMATION & SAUVEGARDE BRONZE
    # (Rappel : C'est transform_save qui va en interne appeler save_to_bronze dès qu'elle aura créé le DataFrame)
    logging.info("Lancement des transformations (Bronze & préparation Silver)...")
    fact_stats, dim_anime = transform_save(liste_brute)
    logging.info("Données transformées avec succès.")
    
    # 4. SAUVEGARDE SILVER
    logging.info("Sauvegarde des tables de Faits et Dimensions dans le catalogue Delta...")
    zone_silver(dim_anime, fact_stats)
    
    logging.info("🎉 Processus terminé avec succès sur Databricks !")