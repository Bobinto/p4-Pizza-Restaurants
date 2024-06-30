from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates


db = SQLAlchemy()

class Pizza(db.Model):
    __tablename__ = 'pizzas'


    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)


class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizzas'


    id = db.Column(db.String, primary_key=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    price = db.Column(db.Integer)


    @hybrid_property
    def is_price_valid(self):
        return self.price is not None and 1 <= self.price <= 30


    @validates('price')
    def validate_price(self, key, price):
        if not self.is_price_valid:
            raise ValueError("Price must be between 1 and 30")
        return price
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)


    pizza = db.relationship('Pizza', backref='restaurant_pizzas')
    restaurant = db.relationship('Restaurant', backref='restaurant_pizzas')


class Restaurant(db.Model):
    __tablename__ = 'restaurants'


    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, unique=True)


    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Restaurant must have a name")
        if len(name) > 50:
            raise ValueError("Restaurant name must be less than 50 characters")
        return name

    address = db.Column(db.String)
