import random
import requests
from bs4 import BeautifulSoup
import openai
from config import Config

openai.api_key = Config.OPENAI_API_KEY

def generate_meal_plan(user, preference, date):
    # This is a simplified example.  In a real app, you'd use the user's
    # preferences to query a database of recipes or call an external API.

    # Example using OpenAI to get recipe suggestions.
    prompt = f"Suggest a meal plan for {date} for a person with dietary restrictions: {preference.dietary_restriction}, allergies: {preference.allergies} and budget: {preference.budget}."
    try:
        completion = openai.Completion.create(
            engine="text-davinci-003", # Or another suitable model
            prompt=prompt,
            max_tokens=300, # Adjust as needed
            n=1,
            stop=None,
            temperature=0.7,
        )
        meal_plan_text = completion.choices[0].text.strip()
        # Parse the OpenAI output (This will be very dependent on the output format)
        # For this example, let's assume it returns:
        # Breakfast: Recipe Name (calories) - Ingredients
        # Lunch: ...
        # Dinner: ...
        meal_plan = {}
        for line in meal_plan_text.split('\n'):
            if ':' in line:
                meal_name, recipe_info = line.split(':', 1)
                meal_name = meal_name.strip()
                recipe_info = recipe_info.strip()
                recipe_name = recipe_info.split('(')[0].strip() if '(' in recipe_info else recipe_info
                #Call function to scrape ingredients
                recipe_details = scrape_recipe(recipe_name)
                meal_plan[meal_name] = recipe_details # Recipe name is enough for now

        return meal_plan
    except Exception as e:
        print(f"Error during OpenAI API call: {e}")
        return None

def scrape_recipe(recipe_name):
    # Example using web scraping (BeautifulSoup) to fetch recipe details.
    # This is a basic example and may need adjustments based on the target website.
    search_query = recipe_name.replace(" ", "+")
    search_url = f"https://www.allrecipes.com/search?q={search_query}"

    try:
        response = requests.get(search_url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the first recipe link (adjust the selector as needed)
        recipe_link = soup.find('a', class_='mntl-card-list-items') #Adjust the tag and class to real website
        if recipe_link:
            recipe_url = recipe_link['href']
            recipe_response = requests.get(recipe_url)
            recipe_response.raise_for_status()
            recipe_soup = BeautifulSoup(recipe_response.content, 'html.parser')

            # Extract ingredients and instructions (adjust selectors as needed)
            ingredients_list = [item.get_text(strip=True) for item in recipe_soup.find_all('li', class_='mntl-ingredient-list__item')]  #Adjust the tag and class to real website
            instructions_list = [item.get_text(strip=True) for item in recipe_soup.find_all('li', class_='mntl-sc-block-group__item')] #Adjust the tag and class to real website
            calories_element = recipe_soup.find('span', class_ = 'nutrition-summary-facts')
            calories = calories_element.get_text(strip=True) if calories_element else 0

            return {
                'name': recipe_name,
                'ingredients': '\n'.join(ingredients_list),
                'instructions': '\n'.join(instructions_list),
                'calories': calories
            }
        else:
            print(f"No recipe found for {recipe_name}")
            return {
                'name': recipe_name,
                'ingredients': 'Ingredients not found',
                'instructions': 'Instructions not found',
                'calories': 0
            }

    except requests.exceptions.RequestException as e:
        print(f"Error during web scraping for {recipe_name}: {e}")
        return {
                'name': recipe_name,
                'ingredients': 'Ingredients not found',
                'instructions': 'Instructions not found',
                'calories': 0
            }