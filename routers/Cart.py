class Cart:
    def __init__(self, item, price):
        self.items = [item]
        self.total = price
        self.quantity = {}
        self.quantity[item] = 1
        self.order_id = None

    def add_item(self, item, price):
        self.total += price
        if item in self.quantity:
            self.quantity[item] += 1
        else:
            self.items.append(item)
            self.quantity[item] = 1

    def get_items(self):
        items = ""
        for item in self.items:
            items += f"{item} x{self.quantity[item]}\n"
        return items
    
    def save_items(self):
        items = ""
        for item in self.items:
            items += f"{item} x{self.quantity[item]} "
        return items

    def get_total(self):
        return self.total
    

cart = {}