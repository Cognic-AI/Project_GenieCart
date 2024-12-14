class MachineCustomer:
    def __init__(self, customer_id, item_name, price_level, tags=[], isHistory = False):
        self.customer_id = customer_id
        self.price_level = price_level
        self.item_name = item_name
        self.tags = tags
        self.history = []
        self.isHistory = isHistory

class Item:
    def __init__(self, name, price, description, link, rate, tags, quantity = 0):
        self.name = name
        self.price = price
        self.description = description
        self.link = link
        self.rate = rate
        self.tags = tags #list of tags [material, style, color, size, etc]
        self.score = 0
        self.quantity = quantity

class Customer:
    def __init__(self, customer_id, customer_name):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.history = []