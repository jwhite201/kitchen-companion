from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import openai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Load your API keys from environment variables
SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

@app.route('/')
def home():
    return "Kitchen Companion is live!"

# GPT Assistant Endpoint
@app.route('/ask_gpt', methods=['POST'])
def ask_gpt():
    data = request.get_json()
    user_input = data.get('message')

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are The Kitchen Companion, a smart and helpful AI chef assistant. Always suggest healthy, realistic, and inspiring ideas."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Recipe Search Endpoint
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
        'apiKey': SPOONACULAR_API_KEY
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

# Recipe Details Endpoint
@app.route('/get_recipe_details', methods=['GET'])
def get_recipe_details():
    recipe_id = request.args.get('id')

    if not recipe_id:
        return jsonify({'error': 'Missing id parameter'}), 400

    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
    params = {'apiKey': SPOONACULAR_API_KEY}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'API call failed', 'details': response.text}), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
