from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Spoonacular API Key loaded from environment
API_KEY = os.getenv('SPOONACULAR_API_KEY')

@app.route('/')
def home():
    return "Welcome to The Kitchen Companion API!"

@app.route('/search_recipes', methods=['GET'])
def search_recipes():
    query = request.args.get('query')
    diet = request.args.get('diet')
    max_ready_time = request.args.get('maxReadyTime')
    number = request.args.get('number', default=5)

    if not query:
        return jsonify({'error': 'Missing query parameter'}), 400

    url = 'https://api.spoonacular.com/recipes/complexSearch'
    params = {
        'query': query,
        'number': number,
        'apiKey': API_KEY
    }

    if diet:
        params['diet'] = diet
    if max_ready_time:
        params['maxReadyTime'] = max_ready_time

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'API call failed', 'details': response.text}), response.status_code
@app.route('/get_recipe_details', methods=['GET'])
def get_recipe_details():
    recipe_id = request.args.get('id')
    if not recipe_id:
        return jsonify({'error': 'Missing id parameter'}), 400

    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
    params = {'apiKey': API_KEY}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'API call failed', 'details': response.text}), response.status_code

@app.route('/substitute', methods=['GET'])
def find_substitute():
    ingredient_name = request.args.get('ingredient')
    
    if not ingredient_name:
        return jsonify({'error': 'Missing ingredient parameter'}), 400

    url = 'https://api.spoonacular.com/food/ingredients/substitutes'
    params = {
        'apiKey': API_KEY,
        'ingredientName': ingredient_name
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'API call failed', 'details': response.text}), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)


