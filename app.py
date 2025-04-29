from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Kitchen Companion is live!"

@app.route('/ask_gpt', methods=['POST'])
def ask_gpt():
    openai.api_key = os.getenv("OPENAI_API_KEY")

    data = request.get_json()
    user_input = data.get('message')

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are The Kitchen Companion, a smart and helpful AI chef assistant. Always suggest healthy, realistic, and inspiring ideas."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response['choices'][0]['message']['content']
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
