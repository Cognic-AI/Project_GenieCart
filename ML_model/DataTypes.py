class MachineCustomer:
    def __init__(self, customer_id, item_name, price_level, tags=[], customer_name=None, email=None, country=None):
        self.customer_id = customer_id
        self.price_level = price_level
        self.item_name = item_name
        self.tags = tags
        self.history = []
        self.customer_name = customer_name
        self.email = email
        self.country = country


class Item:
    def __init__(self, name, price, description, link, rate, tags, image_link=None, currency=None):
        self.name = name
        self.price = price
        self.description = description
        self.link = link
        self.rate = rate
        self.tags = tags #list of tags [material, style, color, size, etc]
        self.score = 0
        self.image_link = image_link
        self.currency = currency

class Customer:
    def __init__(self, customer_id, customer_name):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.history = []