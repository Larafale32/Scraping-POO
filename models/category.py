class Category:
    def __init__(self, name, books):
        self.name = name
        self.books = []

    def add_book(self, book):
        self.books.append(book)