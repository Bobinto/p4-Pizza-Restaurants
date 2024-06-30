# p4-Pizza-Restaurants
### Pizza Restaurant API

This repository contains a Flask backend application and a React frontend application for managing Pizza Restaurants. Below are instructions for setting up and using the project.

### Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. **Install Dependencies**

   Use `pipenv` to manage Python dependencies and `npm` for frontend dependencies.

   ```bash
   pipenv install
   pipenv shell
   npm install --prefix client
   ```

3. **Set Environment Variables**

   Set the `FLASK_APP` environment variable to point to the Flask application.

   ```bash
   export FLASK_APP=server.app
   ```

4. **Database Setup**

   Initialize and migrate the database using Flask-Migrate. Run the following commands:

   ```bash
   flask db init
   flask db migrate
   flask db upgrade head
   ```

   Seed the database with initial data:

   ```bash
   python server/seed.py
   ```

   If needed, modify `server/seed.py` to customize seed data.

5. **Run the Applications**

   Start the Flask API on `localhost:5555`:

   ```bash
   python server/app.py
   ```

   Start the React frontend on `localhost:4000` (optional):

   ```bash
   npm start --prefix client
   ```

   Note: React is for testing API behavior; updates are not required.

### Testing and API Interaction

- **Postman Collection**

  Use the provided Postman collection (`challenge-1-pizzas.postman_collection.json`) to test API routes. Import it into Postman to get started.

  1. Open Postman.
  2. Click Import > Upload Files.
  3. Navigate to the repository folder and select `challenge-1-pizzas.postman_collection.json`.

- **Testing with pytest**

  Run tests with pytest to ensure functionality:

  ```bash
  pytest -x
  ```

### API Routes

#### Restaurants

- **GET `/restaurants`**

  Returns a list of restaurants in JSON format.

- **GET `/restaurants/<int:id>`**

  Returns details of a restaurant by ID. Includes associated pizzas.

- **DELETE `/restaurants/<int:id>`**

  Deletes a restaurant by ID. Cascades to associated restaurant pizzas.

#### Pizzas

- **GET `/pizzas`**

  Returns a list of pizzas in JSON format.

#### RestaurantPizzas

- **POST `/restaurant_pizzas`**

  Creates a new restaurant pizza association. Requires `price`, `pizza_id`, and `restaurant_id` in the request body.

### Validations

- Validations for `RestaurantPizza` model include ensuring price is between 1 and 30.

### Additional Notes

- The frontend is available to interact with the API for realistic testing.

For further assistance or issues, please refer to the project documentation or contact support.

