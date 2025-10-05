import os
import requests
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

# --- App Configuration ---
# Tells Flask to look for all files in the current directory '.'
app = Flask(__name__, template_folder='.', static_folder='.')

# In chatbot.py, right after app = Flask(__name__)

frontend_url = "https://cosmic-tales-frontend.onrender.com"
CORS(app, resources={r"/chat": {"origins": frontend_url}})

# --- API Key and Model Configuration ---
API_KEY = os.getenv('OPENROUTER_API_KEY')
if not API_KEY:
    raise ValueError("No OPENROUTER_API_KEY set. Please check your .env file.")

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "nvidia/nemotron-nano-9b-v2:free"

def format_history_for_openai(history):
    """Converts front-end history to the OpenAI/OpenRouter format."""
    formatted_messages = []
    for message in history:
        role = "assistant" if message['role'] == 'model' else message['role']
        content = message['parts'][0]['text']
        formatted_messages.append({"role": role, "content": content})
    return formatted_messages

# --- Routes to Serve Your Website Files ---

@app.route('/')
def home():
    """Serves the main index.html page."""
    return render_template('index.html')

@app.route('/index.css')
def serve_css():
    """Serves the CSS file."""
    return send_from_directory('.', 'index.css')

@app.route('/index.js')
def serve_js():
    """Serves the JavaScript file."""
    return send_from_directory('.', 'index.js')


# --- Main Chatbot API Endpoint ---

@app.route('/chat', methods=['POST'])
def chat():
    """Handles chat requests from the frontend."""
    try:
        data = request.json
        conversation_history = data.get('conversationHistory', [])

        if not conversation_history:
            return jsonify({"error": "No conversation history provided"}), 400

        messages = format_history_for_openai(conversation_history)
        
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://your-app-name.onrender.com", # Optional: Referer for OpenRouter
            "X-Title": "Cosmic Tales Chatbot" # Optional: Title for OpenRouter
        }
        
        payload = {
            "model": MODEL_NAME,
            "messages": messages,
            "max_tokens": 1024
        }
        
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        response_data = response.json()

        bot_response = response_data['choices'][0]['message']['content']
        
        final_response = {
            "candidates": [{"content": {"parts": [{"text": bot_response}]}}]
        }
        
        return jsonify(final_response)

    except requests.exceptions.RequestException as e:
        error_message = f"API Request Error: {str(e)}"
        if e.response is not None:
              error_message = f"API Request Failed: {e.response.status_code} - {e.response.text}"
        print(error_message)
        return jsonify({"error": error_message}), 500

# --- For Local Testing Only ---

if __name__ == '__main__':
    # This block is only used when you run `python chatbot.py` on your own computer.
    # It is NOT used by Gunicorn on the Render server.
    app.run(host='0.0.0.0', port=5000, debug=True)