import os
import csv
from ..utils.helpers import clean_price


class View:

    def instructions(self):
        print(
            "\nBienvenue sur le service de surveillance du site 'Books to Scrape'.\n"
            "Voici les commandes que vous pouvez exécuter :\n"
            "  1 livre <URL du livre>          : Afficher les informations sur un livre.\n"
            "  2 category <Nom de la catégorie> : Afficher les informations de tous les livres d'une catégorie.\n"
            "  3 all_books <Nombre de pages>     : Afficher les informations de tous les livres.\n"
            "  4 all_images <Nombre de pages>       : Télécharger toutes les images des livres du site.\n"
            "\nExemples :\n"
            "  python3 main.py livre http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html\n"
            "  python3 main.py category fantasy_19 \n"
            "  python3 main.py all_books 50\n"
            "  python3 main.py all_images 50\n"
        )

    def save_to_csv(self, filename, data):
        """Sauvegarde les données dans un fichier CSV."""
        data_folder = '/Users/arnauddekertanguy/Documents/openclassrooms/Projets-Soutenance/Porjet1-Prg-Extraction-des-prix/data'

        # Créer le dossier 'data' s'il n'existe pas
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)

        # Construire le chemin complet du fichier CSV
        file_path = os.path.join(data_folder, filename)
        # Créer le dossier s'il n'existe pas
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # Écrire les en-têtes des colonnes
            writer.writerow(["Numéro", "Image", "Titre", "Prix", "in_stock", "star", "upc",
                             "product_type", "price_without_tx", "price_with_tx", "tx", "review"])

            # Ajouter un compteur pour la numérotation des livres
            for index, row in enumerate(data, start=1):
                # Nettoyer les prix dans les colonnes nécessaires
                row[2] = clean_price(row[2])  # Prix principal
                row[7] = clean_price(row[7])  # Prix sans taxe
                row[8] = clean_price(row[8])  # Prix avec taxe
                row[9] = clean_price(row[9])  # Taxe

                # Écrire la ligne nettoyée
                writer.writerow([index] + row)

        os.system(f"open {filename}")