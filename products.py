# Curtis Saunders, Final Project, CIS 345, 10:30
import json


class Products:

    def __init__(self, prod_id='0000', description='', quantity=0, price=0.0):
        """Initializes variables of Products"""
        self._prod_id = prod_id
        self._description = description
        self._quantity = quantity
        self._price = price

    @property
    def prod_id(self):
        return self._prod_id

    @prod_id.setter
    def prod_id(self, new_id):
        self._prod_id = new_id

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, new_desc):
        self._description = new_desc

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, new_quantity):
        self._quantity = new_quantity

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price):
        self._price = new_price


class Attachables(Products):

    def __init__(self, prod_id='0000', description='', quantity=0, price=0.0, attach_id='0000', material=''):
        """Two new variables: Material, and Attachable ID"""
        super().__init__(prod_id, description, quantity, price)
        self._attach_id = attach_id
        self._material = material

    @property
    def attach_id(self):
        return self._attach_id

    @attach_id.setter
    def attach_id(self, new_id):
        self._attach_id = new_id

    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, mat_type):
        self._material = mat_type


product1 = Products('0023', 'Electric Can Opener', 12, 17.99)
product2 = Products('0101', 'German Beechwood Rolling Pin', 15, 12.99)
product3 = Products('5032', 'Cooling Rack (11 x 16 Inch)', 14, 14.99)
product4 = Products('3078', 'Copper Cooking Pot', 23, 22.99)
product5 = Products('9023', 'Cuisinart Box Grater', 18, 13.99)
product6 = Products('2216', 'Coffee Grinder', 20, 19.99)
product7 = Products('4891', '3-Piece Glass Mixing Bowls', 21, 24.99)
attach1 = Attachables('3080', 'Clip-On Strainer', 13, 8.99, '3078', 'Plastic')
attach2 = Attachables('4900', 'Plastic Lid', 16, 5.99, '4891', 'Plastic')
attach3 = Attachables('9000', 'Storage Measuring Cup', 8, 6.99, '9023', 'Plastic')
attach4 = Attachables('2218', 'Spice Grinder', 9, 11.99, '2216', 'Steel')

# Creating of json file
'''
prod_list = [product1, product2, product3, product4, product5, product6, product7]
attach_list = [attach1, attach2, attach3, attach4]
product_dict = {}

for x in prod_list:
    key = x.prod_id
    product_dict[key] = [x.description, x.quantity, x.price]

for x in attach_list:
    key = x.prod_id
    product_dict[key] = [x.description, x.quantity, x.price, x.attach_id, x.material]

print(product_dict)

with open('products.json', 'w') as fp:
    json.dump(product_dict, fp)
'''