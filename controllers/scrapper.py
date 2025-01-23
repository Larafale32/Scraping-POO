from..views.view import View
from..models.livre import Livre
import sys

class ControllerScrapper:
    def __init__(self, ):
        self.model = Livre()
        self.view = View()

    def run(self):
        print("Début du programme")

        # vérification que le nombre d'argument est suffisant
        if len(sys.argv) < 2:  # On vérifie s'il y a assez d'arguments (au moins 1 argument après le nom du script)
            print("Arguments manquants. Voici comment utiliser le programme :")
            self.view.instructions()  # Affiche les instructions (s'il n'y a pas assez d'arguments)
            return
        # Création de la variable action
        action = sys.argv[1]  # représente le premier argument passé après le nom du script
        print("Action :", action)

        # Vérification que l'actiuon figure bien dans les propositions'
        if action not in ["livre", "category", "all_books", "all_images"]:
            print("Action non reconnue.")
            self.view.instructions()
            return

        if action == "1" and len(sys.argv) < 3:  # Vérifie si l'URL est manquante pour l'action 1
            print("URL manquante pour l'action 1.")
            return

        # crétion de la variable param pour y stocker l'URL
        param = sys.argv[2]  # L'URL est le deuxieme argements passé dans le terminal
        print("Action :", action, ", Paramètre :", param)

        # Appel des fonctions en fonction de l'action'
        if action == "livre":
            print("Exécution de l'action 1")
            url_livre = param
            book_data = self.model.find_book(url_livre)
            print("Données du livre :", book_data)
            csv_filename = "info_livre.csv"
            self.view.save_to_csv(csv_filename, book_data)

        elif action == "category":
            print("Exécution de l'action 2")
            category = param
            print("Catégorie :", category)
            self.model.find_books("http://books.toscrape.com/catalogue/category/books/", category)

        elif action == "all_books":
            print("Exécution de l'action 3")
            self.model.find_all_books()

        elif action == "all_images":
            print("Exécution de l'action 4")
            num_pages = int(param)
            self.model.find_all_images(num_pages)


