from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    preferences = db.relationship('Preference', backref='user', lazy=True)
    meal_plans = db.relationship('MealPlan', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Preference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    dietary_restriction = db.Column(db.String(120))
    allergies = db.Column(db.String(255))
    budget = db.Column(db.Float)

    def __repr__(self):
        return f'<Preference {self.id}>'

class MealPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    meals = db.relationship('Meal', backref='meal_plan', lazy=True)

    def __repr__(self):
        return f'<MealPlan {self.date}>'

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meal_plan_id = db.Column(db.Integer, db.ForeignKey('meal_plan.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id')) # Assuming recipes are stored in the database.

    def __repr__(self):
        return f'<Meal {self.name}>'

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    ingredients = db.Column(db.Text)
    instructions = db.Column(db.Text)
    calories = db.Column(db.Float)
    # Add other nutritional information here

    def __repr__(self):
        return f'<Recipe {self.name}>'

class ShoppingListItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Float)
    unit = db.Column(db.String(50))
    meal_plan_id = db.Column(db.Integer, db.ForeignKey('meal_plan.id'))

    def __repr__(self):
        return f'<ShoppingListItem {self.item_name}>'