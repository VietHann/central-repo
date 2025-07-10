from flask import Blueprint, request, jsonify
from models import db, User, Preference, MealPlan, Meal, Recipe, ShoppingListItem
from datetime import date
from utils import generate_meal_plan, scrape_recipe # Import your utility functions

api = Blueprint('api', __name__)

@api.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'message': 'Missing required fields'}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400

    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        return jsonify({'message': 'Email already exists'}), 400

    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Missing required fields'}), 400

    user = User.query.filter_by(username=username, password=password).first()
    if not user:
        return jsonify({'message': 'Invalid username or password'}), 401

    return jsonify({'message': 'Login successful'}), 200

@api.route('/preferences', methods=['POST'])
def update_preferences():
    data = request.get_json()
    user_id = data.get('user_id')
    dietary_restriction = data.get('dietary_restriction')
    allergies = data.get('allergies')
    budget = data.get('budget')

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    preference = Preference.query.filter_by(user_id=user_id).first()
    if preference:
        preference.dietary_restriction = dietary_restriction
        preference.allergies = allergies
        preference.budget = budget
    else:
        preference = Preference(user_id=user_id, dietary_restriction=dietary_restriction, allergies=allergies, budget=budget)
        db.session.add(preference)

    db.session.commit()

    return jsonify({'message': 'Preferences updated successfully'}), 200

@api.route('/meal_plan', methods=['POST'])
def create_meal_plan():
    data = request.get_json()
    user_id = data.get('user_id')
    date_str = data.get('date') # Expecting date in ISO format (YYYY-MM-DD)
    try:
        date_obj = date.fromisoformat(date_str)
    except ValueError:
        return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    preference = Preference.query.filter_by(user_id=user_id).first()
    if not preference:
        return jsonify({'message': 'User preferences not found'}), 400

    # Call the utility function to generate the meal plan.
    meal_plan_data = generate_meal_plan(user, preference, date_obj)
    if not meal_plan_data:
        return jsonify({'message': 'Failed to generate meal plan'}), 500

    new_meal_plan = MealPlan(user_id=user_id, date=date_obj)
    db.session.add(new_meal_plan)
    db.session.flush()  # Get the new_meal_plan.id

    for meal_name, recipe_details in meal_plan_data.items():
        # Check if the recipe exists, if not, add it
        recipe = Recipe.query.filter_by(name=recipe_details['name']).first()
        if not recipe:
            # Assuming recipe_details contains ingredients and instructions
            recipe = Recipe(name=recipe_details['name'], ingredients=recipe_details['ingredients'], instructions=recipe_details['instructions'], calories=recipe_details['calories'])
            db.session.add(recipe)
            db.session.flush()

        new_meal = Meal(meal_plan_id=new_meal_plan.id, name=meal_name, recipe_id=recipe.id)
        db.session.add(new_meal)

    #Generate shopping list
    shopping_list = {}
    for meal_name, recipe_details in meal_plan_data.items():
        ingredients_list = recipe_details['ingredients'].split('\n')
        for item in ingredients_list:
            item = item.strip()
            if item:  # Ensure the item is not empty
                if item in shopping_list:
                    shopping_list[item] +=1
                else:
                    shopping_list[item] = 1

    for item, quantity in shopping_list.items():
        shopping_item = ShoppingListItem(meal_plan_id=new_meal_plan.id, item_name=item, quantity = quantity, unit = "")
        db.session.add(shopping_item)

    db.session.commit()

    return jsonify({'message': 'Meal plan created successfully', 'meal_plan_id': new_meal_plan.id}), 201


@api.route('/meal_plan/<int:meal_plan_id>', methods=['GET'])
def get_meal_plan(meal_plan_id):    
    meal_plan = MealPlan.query.get(meal_plan_id)
    if not meal_plan:
        return jsonify({'message': 'Meal plan not found'}), 404

    meals = Meal.query.filter_by(meal_plan_id=meal_plan_id).all()
    meal_data = []
    for meal in meals:
        recipe = Recipe.query.get(meal.recipe_id)
        if recipe:
          meal_data.append({
              'meal_name': meal.name,
              'recipe_name': recipe.name,
              'recipe_ingredients': recipe.ingredients,
              'recipe_instructions': recipe.instructions,    
              'recipe_calories': recipe.calories
          })
        else:
          meal_data.append({
              'meal_name': meal.name,
              'recipe_name': 'Recipe Not Found',
              'recipe_ingredients': '',
              'recipe_instructions': '',
              'recipe_calories': 0
          })


    shopping_list_items = ShoppingListItem.query.filter_by(meal_plan_id=meal_plan_id).all()
    shopping_list = [{'item_name': item.item_name, 'quantity': item.quantity, 'unit': item.unit} for item in shopping_list_items]

    return jsonify({
        'date': str(meal_plan.date),
        'meals': meal_data,
        'shopping_list': shopping_list
    }), 200


@api.route('/recipe/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({'message': 'Recipe not found'}), 404
    return jsonify({
        'name': recipe.name,
        'ingredients': recipe.ingredients,
        'instructions': recipe.instructions,
        'calories': recipe.calories
    }), 200