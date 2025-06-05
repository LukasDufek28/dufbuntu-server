from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness.db'
db = SQLAlchemy(app)

# Food database
class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    calories = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    carbs = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)

# User meal log
class MealLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)  # YYYY-MM-DD
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)  # in grams

def setup():
    db.create_all()
    if Food.query.count() == 0:
        foods_data = [
            {"name": "Apple", "calories": 52, "protein": 0.3, "carbs": 14, "fat": 0.2},
            {"name": "Banana", "calories": 89, "protein": 1.1, "carbs": 23, "fat": 0.3},
            {"name": "Chicken Breast", "calories": 165, "protein": 31, "carbs": 0, "fat": 3.6},
            {"name": "Broccoli", "calories": 34, "protein": 2.8, "carbs": 7, "fat": 0.4},
            {"name": "White Rice", "calories": 130, "protein": 2.7, "carbs": 28, "fat": 0.3},
            {"name": "Egg", "calories": 155, "protein": 13, "carbs": 1.1, "fat": 11},
            {"name": "Salmon", "calories": 208, "protein": 20, "carbs": 0, "fat": 13},
            {"name": "Potato", "calories": 77, "protein": 2, "carbs": 17, "fat": 0.1},
            {"name": "Almonds", "calories": 579, "protein": 21, "carbs": 22, "fat": 50},
            {"name": "Oats", "calories": 389, "protein": 17, "carbs": 66, "fat": 7},
            {"name": "Cheddar Cheese", "calories": 403, "protein": 25, "carbs": 1.3, "fat": 33},
            {"name": "Greek Yogurt", "calories": 59, "protein": 10, "carbs": 3.6, "fat": 0.4},
            {"name": "Spinach", "calories": 23, "protein": 2.9, "carbs": 3.6, "fat": 0.4},
            {"name": "Carrot", "calories": 41, "protein": 0.9, "carbs": 10, "fat": 0.2},
            {"name": "Orange", "calories": 47, "protein": 0.9, "carbs": 12, "fat": 0.1},
            {"name": "Beef Steak", "calories": 271, "protein": 25, "carbs": 0, "fat": 19},
            {"name": "Brown Rice", "calories": 123, "protein": 2.7, "carbs": 25.6, "fat": 1},
            {"name": "Avocado", "calories": 160, "protein": 2, "carbs": 9, "fat": 15},
            {"name": "Peanut Butter", "calories": 588, "protein": 25, "carbs": 20, "fat": 50},
            {"name": "Milk", "calories": 42, "protein": 3.4, "carbs": 5, "fat": 1},
            {"name": "Tofu", "calories": 76, "protein": 8, "carbs": 1.9, "fat": 4.8},
            {"name": "Quinoa", "calories": 120, "protein": 4.1, "carbs": 21.3, "fat": 1.9},
            {"name": "Sweet Potato", "calories": 86, "protein": 1.6, "carbs": 20.1, "fat": 0.1},
            {"name": "Lentils", "calories": 116, "protein": 9, "carbs": 20, "fat": 0.4},
            {"name": "Chickpeas", "calories": 164, "protein": 8.9, "carbs": 27.4, "fat": 2.6},
            {"name": "Turkey Breast", "calories": 135, "protein": 30, "carbs": 0, "fat": 1},
            {"name": "Cottage Cheese", "calories": 98, "protein": 11, "carbs": 3.4, "fat": 4.3},
            {"name": "Blueberries", "calories": 57, "protein": 0.7, "carbs": 14, "fat": 0.3},
            {"name": "Strawberries", "calories": 32, "protein": 0.7, "carbs": 7.7, "fat": 0.3},
            {"name": "Raspberries", "calories": 52, "protein": 1.2, "carbs": 11.9, "fat": 0.7},
            {"name": "Black Beans", "calories": 132, "protein": 8.9, "carbs": 23.7, "fat": 0.5},
            {"name": "Green Peas", "calories": 81, "protein": 5.4, "carbs": 14.5, "fat": 0.4},
            {"name": "Zucchini", "calories": 17, "protein": 1.2, "carbs": 3.1, "fat": 0.3},
            {"name": "Cucumber", "calories": 16, "protein": 0.7, "carbs": 3.6, "fat": 0.1},
            {"name": "Tomato", "calories": 18, "protein": 0.9, "carbs": 3.9, "fat": 0.2},
            {"name": "Cauliflower", "calories": 25, "protein": 1.9, "carbs": 5, "fat": 0.3},
            {"name": "Mushrooms", "calories": 22, "protein": 3.1, "carbs": 3.3, "fat": 0.3},
            {"name": "Pineapple", "calories": 50, "protein": 0.5, "carbs": 13.1, "fat": 0.1},
            {"name": "Mango", "calories": 60, "protein": 0.8, "carbs": 15, "fat": 0.4},
            {"name": "Grapes", "calories": 69, "protein": 0.7, "carbs": 18.1, "fat": 0.2},
            {"name": "Watermelon", "calories": 30, "protein": 0.6, "carbs": 7.6, "fat": 0.2},
            {"name": "Peach", "calories": 39, "protein": 0.9, "carbs": 9.5, "fat": 0.3},
            {"name": "Pear", "calories": 57, "protein": 0.4, "carbs": 15, "fat": 0.1},
            {"name": "Plum", "calories": 46, "protein": 0.7, "carbs": 11.4, "fat": 0.3},
            {"name": "Chia Seeds", "calories": 486, "protein": 17, "carbs": 42, "fat": 31},
            {"name": "Pumpkin Seeds", "calories": 559, "protein": 30, "carbs": 11, "fat": 49},
            {"name": "Flax Seeds", "calories": 534, "protein": 18, "carbs": 29, "fat": 42},
            {"name": "Cashews", "calories": 553, "protein": 18, "carbs": 30, "fat": 44},
            {"name": "Walnuts", "calories": 654, "protein": 15, "carbs": 14, "fat": 65},
            {"name": "Hazelnuts", "calories": 628, "protein": 15, "carbs": 17, "fat": 61},
            {"name": "Macadamia Nuts", "calories": 718, "protein": 8, "carbs": 14, "fat": 76},
            {"name": "Sunflower Seeds", "calories": 584, "protein": 21, "carbs": 20, "fat": 51},
            {"name": "Dates", "calories": 282, "protein": 2.5, "carbs": 75, "fat": 0.4},
            {"name": "Figs", "calories": 74, "protein": 0.8, "carbs": 19, "fat": 0.3},
            {"name": "Kiwi", "calories": 41, "protein": 0.8, "carbs": 10.1, "fat": 0.4},
            {"name": "Cranberries", "calories": 46, "protein": 0.4, "carbs": 12.2, "fat": 0.1},
            {"name": "Cabbage", "calories": 25, "protein": 1.3, "carbs": 5.8, "fat": 0.1},
            {"name": "Eggplant", "calories": 25, "protein": 1, "carbs": 6, "fat": 0.2},
            {"name": "Green Beans", "calories": 31, "protein": 1.8, "carbs": 7, "fat": 0.1},
            {"name": "Beetroot", "calories": 43, "protein": 1.6, "carbs": 10, "fat": 0.2},
            {"name": "Asparagus", "calories": 20, "protein": 2.2, "carbs": 3.9, "fat": 0.1},
            {"name": "Bell Pepper", "calories": 31, "protein": 1, "carbs": 6, "fat": 0.3},
            {"name": "Onion", "calories": 40, "protein": 1.1, "carbs": 9.3, "fat": 0.1},
            {"name": "Garlic", "calories": 149, "protein": 6.4, "carbs": 33, "fat": 0.5},
            {"name": "Leek", "calories": 61, "protein": 1.5, "carbs": 14, "fat": 0.3},
            {"name": "Celery", "calories": 16, "protein": 0.7, "carbs": 3, "fat": 0.2},
            {"name": "Radish", "calories": 16, "protein": 0.7, "carbs": 3.4, "fat": 0.1},
            {"name": "Turnip", "calories": 28, "protein": 0.9, "carbs": 6.4, "fat": 0.1},
            {"name": "Artichoke", "calories": 47, "protein": 3.3, "carbs": 11, "fat": 0.2},
            {"name": "Parsnip", "calories": 75, "protein": 1.2, "carbs": 18, "fat": 0.3},
            {"name": "Okra", "calories": 33, "protein": 2, "carbs": 7.5, "fat": 0.2},
            {"name": "Brussels Sprouts", "calories": 43, "protein": 3.4, "carbs": 9, "fat": 0.3},
            {"name": "Seaweed", "calories": 45, "protein": 5.8, "carbs": 8, "fat": 0.6},
            {"name": "Soy Milk", "calories": 54, "protein": 3.3, "carbs": 6.3, "fat": 1.8},
            {"name": "Coconut Milk", "calories": 230, "protein": 2.3, "carbs": 5.5, "fat": 24},
            {"name": "Rice Milk", "calories": 47, "protein": 0.3, "carbs": 9.2, "fat": 1},
            {"name": "Oat Milk", "calories": 43, "protein": 1, "carbs": 6.7, "fat": 1.3},
            {"name": "Beef Liver", "calories": 135, "protein": 20.4, "carbs": 3.9, "fat": 3.6},
            {"name": "Pork Chop", "calories": 231, "protein": 25.7, "carbs": 0, "fat": 13.9},
            {"name": "Duck Breast", "calories": 337, "protein": 23.5, "carbs": 0, "fat": 28.4},
            {"name": "Lamb", "calories": 294, "protein": 25.6, "carbs": 0, "fat": 21.3},
            {"name": "Tuna", "calories": 132, "protein": 28, "carbs": 0, "fat": 1.3},
            {"name": "Herring", "calories": 158, "protein": 18, "carbs": 0, "fat": 9},
            {"name": "Sardines", "calories": 208, "protein": 25, "carbs": 0, "fat": 11},
            {"name": "Shrimp", "calories": 99, "protein": 24, "carbs": 0.2, "fat": 0.3},
            {"name": "Crab", "calories": 97, "protein": 19, "carbs": 0, "fat": 1.5},
            {"name": "Lobster", "calories": 89, "protein": 19, "carbs": 0, "fat": 0.9},
            {"name": "Octopus", "calories": 82, "protein": 14.9, "carbs": 2.2, "fat": 1},
            {"name": "Squid", "calories": 92, "protein": 15.6, "carbs": 3.1, "fat": 1.4},
            # ...add more foods up to 100 as needed...
        ]
        for food in foods_data:
            db.session.add(Food(**food))
        db.session.commit()

@app.route('/api/foods')
def get_foods():
    foods = Food.query.all()
    return jsonify([{
        'id': f.id,
        'name': f.name,
        'calories': f.calories,
        'protein': f.protein,
        'carbs': f.carbs,
        'fat': f.fat
    } for f in foods])

@app.route('/api/log_meal', methods=['POST'])
def log_meal():
    data = request.json
    meal = MealLog(
        date=data['date'],
        food_id=data['food_id'],
        quantity=data['quantity']
    )
    db.session.add(meal)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/daily_summary/<log_date>')
def daily_summary(log_date):
    logs = MealLog.query.filter_by(date=log_date).all()
    summary = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
    for log in logs:
        food = Food.query.get(log.food_id)
        factor = log.quantity / 100.0
        summary['calories'] += food.calories * factor
        summary['protein'] += food.protein * factor
        summary['carbs'] += food.carbs * factor
        summary['fat'] += food.fat * factor
    return jsonify(summary)

@app.route('/api/calendar')
def calendar():
    # Returns a list of days with total nutrients
    days = db.session.query(MealLog.date).distinct().all()
    result = []
    for (log_date,) in days:
        logs = MealLog.query.filter_by(date=log_date).all()
        summary = {'date': log_date, 'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
        for log in logs:
            food = Food.query.get(log.food_id)
            factor = log.quantity / 100.0
            summary['calories'] += food.calories * factor
            summary['protein'] += food.protein * factor
            summary['carbs'] += food.carbs * factor
            summary['fat'] += food.fat * factor
        result.append(summary)
    return jsonify(result)

if __name__ == '__main__':
    with app.app_context():
        setup()
    app.run(host='0.0.0.0', port=5000)
