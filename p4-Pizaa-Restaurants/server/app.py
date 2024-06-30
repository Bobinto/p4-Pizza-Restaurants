from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Restaurant, Pizza, RestaurantPizza

# Create a Flask application
app = Flask(__name__)
# Configure the database URI and disable modification tracking
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database migration
migrate = Migrate(app, db)

# Initialize the database with the Flask app
db.init_app(app)

# Define a route to get all restaurants
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    # Query all restaurants from the database
    restaurants = Restaurant.query.all()
    restaurant_data = []

    # Build a JSON response with restaurant details
    for restaurant in restaurants:
        restaurant_data.append({
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address
        })

    return jsonify(restaurant_data)

# Define a route to get a restaurant by ID
@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    # Query the database to find the restaurant by ID
    restaurant = Restaurant.query.get(id)

    if restaurant is not None:
        # Build the JSON response with restaurant details and its pizzas
        restaurant_data = {
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address,
            "pizzas": []
        }

        # Retrieve and include the pizzas associated with the restaurant
        for restaurant_pizza in restaurant.restaurant_pizzas:
            pizza = restaurant_pizza.pizza
            restaurant_data["pizzas"].append({
                "id": pizza.id,
                "name": pizza.name,
                "ingredients": pizza.ingredients
            })

        return jsonify(restaurant_data)
    else:
        # Return an error message and 404 status code if the restaurant is not found
        return jsonify({"error": "Restaurant not found"}), 404

# Define a route to delete a restaurant by ID
@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    # Query the database to find the restaurant by ID
    restaurant = Restaurant.query.get(id)

    if restaurant is not None:
        # Delete any associated RestaurantPizza entries first
        RestaurantPizza.query.filter_by(restaurant_id=id).delete()

        try:
            # Delete the restaurant
            db.session.delete(restaurant)
            db.session.commit()

            # Return an empty response with a 204 status code
            return '', 204
        except Exception as e:
            # Handle any database errors
            return jsonify({"error": "An error occurred while deleting the restaurant"}), 500
    else:
        # Return an error message and 404 status code if the restaurant is not found
        return jsonify({"error": "Restaurant not found"}), 404

# Define a route to get all pizzas
@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    # Query all pizzas from the database
    pizzas = Pizza.query.all()
    pizza_data = []

    # Build a JSON response with pizza details
    for pizza in pizzas:
        pizza_data.append({
            "id": pizza.id,
            "name": pizza.name,
            "ingredients": pizza.ingredients
        })

    return jsonify(pizza_data)

# Define a route to create a new RestaurantPizza entry
@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    # Retrieve JSON data from the request
    data = request.get_json()

    # Extract properties from the JSON data
    price, pizza_id, restaurant_id = data.get('price'), data.get('pizza_id'), data.get('restaurant_id')
    errors = []

    # Validate the price
    if not (1 <= price <= 30) or not isinstance(price, int):
        errors.append("Price must be an integer between 1 and 30")

    # Query the database for the pizza and restaurant
    pizza = Pizza.query.get(pizza_id) if pizza_id else None
    restaurant = Restaurant.query.get(restaurant_id) if restaurant_id else None

    # Check if the pizza and restaurant exist
    if not pizza:
        errors.append("Pizza not found")
    if not restaurant:
        errors.append("Restaurant not found")

    # Handle validation errors
    if errors:
        return jsonify({"errors": errors}), 400

    # Create a new RestaurantPizza entry
    restaurant_pizza = RestaurantPizza(price=price, pizza=pizza, restaurant=restaurant)

    db.session.add(restaurant_pizza)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 500

    # Return the details of the associated pizza
    return jsonify({
        "id": pizza.id,
        "name": pizza.name,
        "ingredients": pizza.ingredients
    })

if __name__ == '__main__':
    app.run(port=5555)