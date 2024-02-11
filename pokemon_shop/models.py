import requests
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from datetime import datetime
import uuid
from flask_marshmallow import Marshmallow

#internal imports
from .helpers import get_image
from .helpers import get_ability
from .helpers import get_type
from .helpers import get_height
from .helpers import get_weight


db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):

    user_id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())


    def __init__(self, username, email, password, first_name="", last_name=""):
        self.user_id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = self.set_password(password)

    
    def set_id(self):
        return str(uuid.uuid4())
    
    def get_id(self):
        return str(self.user_id)
    
    def set_password(self, password):
        return generate_password_hash(password)
    
    def __repr__(self):
        return f"<User: {self.username}>"
    


class Product(db.Model):
    prod_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String)
    types = db.Column(db.String(50))
    ability = db.Column(db.String)
    height = db.Column(db.String(20))
    weight = db.Column(db.String(20))
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, default = datetime.utcnow())

    def __init__(self, name, price, quantity, image="", types="", ability="", height="", weight=""):
        self.prod_id = self.set_id()
        self.name = name
        self.image = self.set_image(image, name)
        self.types = self.set_types(types, name)
        self.ability = self.set_ability(ability, name)
        self.height = self.set_height(height, name)
        self.weight = self.set_weight(weight, name)
        self.price = price
        self.quantity = quantity
        

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_image(self, image, name):
        if not image:
            image = get_image(name)
        return image
    
    def set_ability(self, ability, name):
        if not ability:
            ability = get_ability(name)
        return ability
    
    def set_types(self, types, name):
        if not types:
            types = get_type(name)
        return types

    def set_height(self, height, name):
        if not height:
            height = get_height(name)
        return height
    
    def set_weight(self, weight, name):
        if not weight:
            weight = get_weight(name)
        return weight    
     
    def decrement_quantity(self, quantity):
        self.quantity -= int(quantity)
        return self.quantity
    
    def increment_quantity(self, quantity):
        self.quantity += int(quantity)
        return self.quantity
    
    def __repr__(self):
        return f"<Pokemon: {self.name}>"
    


class Customer(db.Model):
    cust_id = db.Column(db.String, primary_key=True)
    date_created = db.Column(db.DateTime, default = datetime.utcnow())
    prodord = db.relationship('ProdOrder', backref = 'customer', lazy=True)

    def __init__(self, cust_id):
        self.cust_id = cust_id

    def __repr__(self):
        return f"<Customer: {self.cust_id}>"
    


class ProdOrder(db.Model):
    prodorder_id = db.Column(db.String, primary_key=True)
    prod_id = db.Column(db.String, db.ForeignKey('product.prod_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    order_id = db.Column(db.String, db.ForeignKey('order.order_id'), nullable=False)
    cust_id = db.Column(db.String, db.ForeignKey('customer.cust_id'), nullable=False)

    def __init__(self, prod_id, quantity, price, order_id, cust_id):
        self.prodorder_id = self.set_id()
        self.prod_id = prod_id
        self.quantity = quantity
        self.price = self.set_price(quantity, price)
        self.order_id = order_id
        self.cust_id = cust_id

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_price(self, quantity, price):
        quantity = int(quantity)
        price = float(price)

        self.price = quantity * price
        return self.price
    
    def update_quantity(self, quantity):
        self.quantity = int(quantity)
        return self.quantity



class Order(db.Model):
    order_id = db.Column(db.String, primary_key=True)
    order_total = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    prodord = db.relationship('ProdOrder', backref = 'order', lazy=True)

    def __init__(self):
        self.order_id = self.set_id()
        self.order_total = 0.00

    def set_id(self):
        return str(uuid.uuid4())
    
    def increment_ordertotal(self, price):
        self.order_total = float(self.order_total)
        self.order_total += float(price)
        return self.order_total
    
    def decrement_ordertotal(self, price):
        self.order_total = float(self.order_total)
        self.order_total -= float(price)
        return self.order_total
    
    def __repr__(self):
        return f"<Order: {self.order_id}>"



class PokemonSchema(ma.Schema):
    class Meta:
        fields = ['prod_id', 'name', 'image', 'types', 'ability', 'height', 'weight', 'price', 'quantity']


pokemon_schema = PokemonSchema()
pokemons_schema = PokemonSchema(many=True)





# TRIED ADDING METHOD TO CALL INFORMATION DIRECTLY FROM POKEAPI SITE
# I WAS ABLE TO GET THE INFORMATION, BUT GOT A SQLALCHEMY INTEGRITYERROR AND COULDNT CREATE ITEM
# CAN TRY AGAIN WITH NEW WEIGHT/HEIGHT STRING CHANGE -- ANOTHER TIME

    # def __init__(self, name, price, quantity, image="", types="", ability="", height="", weight=""):
    #     self.name = name
    #     self.price = price
    #     self.quantity = quantity
    #     self.image = image
    #     self.types = []
    #     self.ability = []
    #     self.height = None
    #     self.weight = None
    #     self.poke_api_call()

    # def poke_api_call(self):
    #     r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.name.lower()}")
    #     if r.status_code == 200:
    #         pokemon = r.json()
    #     else:
    #         print(f"Please check Pokemon spelling and try again: {r.status_code}")

    #     self.name = pokemon['name']
    #     self.types = [type_['type']['name'] for type_ in pokemon['types']]
    #     self.ability = [pokebility['ability']['name'] for pokebility in pokemon['abilities']]
    #     self.height = pokemon['height']
    #     self.weight = pokemon['weight']
