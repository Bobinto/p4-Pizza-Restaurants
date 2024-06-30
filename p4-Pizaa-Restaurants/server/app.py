from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    restaurant_data = []

    for restaurant in restaurants:
        restaurant_data.append({
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address
        })

    return jsonify(restaurant_data)

@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)

    if restaurant is not None:
        restaurant_data = {
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address,
            "pizzas": []
        }

        for restaurant_pizza in restaurant.restaurant_pizzas:
            pizza = restaurant_pizza.pizza
            restaurant_data["pizzas"].append({
                "id": pizza.id,
                "name": pizza.name,
                "ingredients": pizza.ingredients
            })

        return jsonify(restaurant_data)
    else:
        return jsonify({"error": "Restaurant not found"}), 404

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)

    if restaurant is not None:
        RestaurantPizza.query.filter_by(restaurant_id=id).delete()

        try:
            db.session.delete(restaurant)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "An error occurred while deleting the restaurant"}), 500
    else:
        return jsonify({"error": "Restaurant not found"}), 404

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    pizza_data = []

    for pizza in pizzas:
        pizza_data.append({
            "id": pizza.id,
            "name": pizza.name,
            "ingredients": pizza.ingredients
        })

    return jsonify(pizza_data)

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()

    price, pizza_id, restaurant_id = data.get('price'), data.get('pizza_id'), data.get('restaurant_id')
    errors = []

    if not (1 <= price <= 30) or not isinstance(price, int):
        errors.append("Price must be an integer between 1 and 30")

    pizza = Pizza.query.get(pizza_id) if pizza_id else None
    restaurant = Restaurant.query.get(restaurant_id) if restaurant_id else None

    if not pizza:
        errors.append("Pizza not found")
    if not restaurant:
        errors.append("Restaurant not found")

    if errors:
        return jsonify({"errors": errors}), 400

    restaurant_pizza = RestaurantPizza(price=price, pizza=pizza, restaurant=restaurant)

    db.session.add(restaurant_pizza)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 500

    return jsonify({
        "id": pizza.id,
        "name": pizza.name,
        "ingredients": pizza.ingredients
    })

if __name__ == '__main__':
    app.run(port=5555)
