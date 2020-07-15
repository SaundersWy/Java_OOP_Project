# Curtis Saunders, Final Project, CIS 345, 10:30


class Orders:

    def __init__(self, item, quantity, price):
        self.__item = item
        self.__quantity = quantity
        self.__price = price
        self.__total_price = float(quantity) * float(price)

    def __str__(self):
        """Overrides String Representation of Order"""
        return f'{self.__item:<35}{int(self.__quantity):<15}${self.__price:<15}${float(self.__total_price):<15.2f}'

    @property
    def item(self):
        return self.__item

    @item.setter
    def item(self, new_item):
        self.__item = new_item

    @property
    def quantity(self):
        return self.__quantity

    @quantity.setter
    def quantity(self, new_quantity):
        self.__quantity = new_quantity

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, new_price):
        self.__item = new_price

    @property
    def total_price(self):
        return self.__total_price

    @total_price.setter
    def total_price(self):
        self.__total_price = float(self.__quantity) * float(self.__price)
