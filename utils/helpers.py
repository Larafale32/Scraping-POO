def clean_price(value):
    """Supprime les caractères indésirables dans les prix."""
    return value.replace("Â", "").replace("£", "").strip()


def clean_stock(stock):
    stock = stock.replace("In stock (", "").replace(" available)", "")
    return stock.strip()


def clean_note(note):
    return note.replace("One", "1").replace("Two", "2").replace("Three", "3").replace("Four", "4").replace("Five", "5")