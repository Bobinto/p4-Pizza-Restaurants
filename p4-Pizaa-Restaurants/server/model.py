from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates

# Create a SQLAlchemy database instance
db = SQLAlchemy()

# Define the Pizza model
class Pizza(db.Model):
    __tablename__ = 'pizzas'

    # Define table columns
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

# Define the RestaurantPizza model
class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizzas'

    # Define table columns
    id = db.Column(db.String, primary_key=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    price = db.Column(db.Integer)

    # Define a hybrid property for price validation
    @hybrid_property
    def is_price_valid(self):
        return self.price is not None and 1 <= self.price <= 30

    # Define a validator for price
    @validates('price')
    def validate_price(self, key, price):
        if not self.is_price_valid:
            raise ValueError("Price must be between 1 and 30")
        return price
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    # Define relationships with Pizza and Restaurant models
    pizza = db.relationship('Pizza', backref='restaurant_pizzas')
    restaurant = db.relationship('Restaurant', backref='restaurant_pizzas')

# Define the Restaurant model
class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    # Define table columns
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, unique=True)

    # Define a validator for restaurant name
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Restaurant must have a name")
        if len(name) > 50:
            raise ValueError("Restaurant name must be less than 50 characters")
        return name

    address = db.Column(db.String)
