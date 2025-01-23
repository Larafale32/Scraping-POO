import csv
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from ..utils.helpers import clean_price, clean_note, clean_stock
from..views.view import View

class Livre:
    def __init__(self):
        self.view = View()

    class Livre:
        def __init__(self, image, titre, prix, star, upc, product_type, price_without_tx, tx, review, in_stock=True):
            self.image = image
            self.titre = titre
            self.prix = prix
            self.star = star
            self.upc = upc
            self.product_type = product_type
            self.price_without_tx = price_without_tx
            self.tx = tx
            self.review = review
            self.in_stock = in_stock

    def find_book(self, url):
        """Récupère les informations d'un livre à partir de son URL."""
        info_livre = []
        response = requests.get(url)
        if response.ok:
            soup = BeautifulSoup(response.text, "html.parser")

            # Récupérer l'image du livre (convertir en URL absolue)
            image_tag = soup.find("img")
            image_url = urljoin(url, image_tag["src"]) if image_tag else ""

            # Récupérer le titre du livre
            title = soup.find("h1").get_text() if soup.find("h1") else ""

            # Récupérer le prix du livre
            price_bis = (
                soup.find("p", class_="price_color").get_text()
                if soup.find("p", class_="price_color")
                else ""
            )
            price = clean_price(price_bis)

            # Récupérer la disponibilité
            in_stock = soup.find("p", class_="instock availability")
            in_stock = in_stock.get_text().strip().replace("\n", "") if in_stock else ""
            in_stock = clean_stock(in_stock)

            # Récupérer la note du livre
            rating = soup.find("p", class_="star-rating")
            star = ""
            if rating:
                star = rating.get("class")[1]
                star = clean_note(star) + "/5"

            # Récupérer les informations produit (UPC, type, prix sans taxes, etc.)
            table = soup.find("table", class_="table table-striped")
            all_tr = table.find_all("tr")
            upc = all_tr[0].find("td").get_text()
            product_type = all_tr[1].find("td").get_text()
            price_without_tx = all_tr[2].find("td").get_text()
            price_without_tx = clean_price(price_without_tx)
            price_with_tx = all_tr[3].find("td").get_text()
            price_with_tx = clean_price(price_with_tx)
            tx = all_tr[4].find("td").get_text()
            review = all_tr[6].find("td").get_text()

            # Ajouter toutes les informations dans info_livre (11 éléments)
            info_livre.append([image_url, title, price, in_stock, star, upc, product_type,
                               price_without_tx, price_with_tx, tx, review])

        return info_livre

    def find_books(self, base_url, category):
        """Récupère les informations des livres d'une catégorie spécifique."""
        all_data = []

        # URL de la catégorie
        category_url = urljoin(base_url, category)
        page_number = 1  # On commence à la première page

        # Boucle pour définir le nombre de pages à scraper
        while True:
            # Construire l'URL de la page actuelle
            page_url = category_url + "/page-" + str(
                page_number) + ".html" if page_number > 1 else category_url + "/index.html"
            print("Accès à la page :", page_url)

            response = requests.get(page_url)  # Récupérer la page
            if not response.ok:  # Si la page n'est pas trouvée, arrêter
                break

            soup = BeautifulSoup(response.text, "html.parser")
            books = soup.find("ol", class_="row")  # Trouver les livres sur la page
            if not books:  # Si aucune liste de livres n'est trouvée, arrêter
                print("Aucune donnée trouvée. Fin du scraping.")
                break

            # Traiter les livres trouvés
            for book in books.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"):
                product_url = urljoin(base_url + "catalogue/", book.find("a")["href"])
                book_data = self.find_book(product_url)
                if book_data:
                    all_data.extend(book_data)

            page_number += 1  # Ajouter 1 à page-number pour passer à la page suivante

        # Sauvegarder les données dans un fichier CSV
        if all_data:
            self.view.save_to_csv("books_info.csv", all_data)
            print("Les données ont été sauvegardées dans 'books_info.csv'.")
        else:
            print("Aucune donnée n'a été récupérée.")

        return all_data

    def find_all_books(self):
        all_data = []
        category = None
        base_url = "http://books.toscrape.com/catalogue/category/books_1"

        all_data.append(self.find_books(base_url, category))

    def find_all_images(self, num_pages=50):
        all_data = []
        base_url = "http://books.toscrape.com/catalogue/category/books_1"
        for i in range(num_pages):

            url = base_url + "/page-" + str(i + 1) + ".html"
            print("Accès à la page " + url)

            response = requests.get(url)
            if response.ok:
                soup = BeautifulSoup(response.text, "html.parser")
                books = soup.find("ol", class_="row")

                if books:
                    books = books.find_all(
                        "li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"
                    )
                    for book in books:
                        image_url = book.find("img").get("src")
                        image_url = urljoin(base_url, image_url)
                        all_data.append(image_url)
                        print(len(all_data))

                        self.download_images(image_url, destination="/Users/arnauddekertanguy/Documents/img_books")

    def download_images(self, url_image, destination):
        # créer un dossier s'il n'existe pas
        if not os.path.exists(destination):
            os.makedirs(destination)

        file_name = url_image.split("/")[-1]
        file_path = os.path.join(destination, file_name)

        response = requests.get(url_image)
        if response.ok:
            # chemin complet vers le fichier
            with open(os.path.join(destination, file_name), "wb") as file:
                file.write(response.content)
                print("Image téléchargée avec succès à l'adresse" + str(file_path))
        else:
            print("Impossible de télécharger l'image à l'URL " + url_image)

