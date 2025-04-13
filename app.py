# app.py
import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from waitress import serve  # ✅ Use waitress for production

app = Flask(__name__)

# ✅ Google API Key (use environment variable if possible)
GOOGLE_API_KEY = "AIzaSyC3paOX0K-SFCSEx7tol1xdb1HeCK9yR4I"

if not GOOGLE_API_KEY:
    print("Error: GOOGLE_API_KEY not set.")
else:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("models/gemini-1.5-pro")

conversation_history = []

def voice_assistance(user_input):
    global conversation_history

    prompt = f"""
    Please provide a professional and concise solution or response to the following user query:
    '{user_input}'
    The answer should be brief, precise, and directly address the request.
    """

    try:
        response = model.generate_content(prompt).text
    except Exception as e:
        print(f"Error generating response: {e}")
        response = "Sorry, I encountered an error processing your request."

    conversation_history.append({'user': user_input, 'ai': response})
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_voice', methods=['POST'])
def process_voice():
    try:
        user_input = request.json.get("user_input")
        if not user_input:
            return jsonify({'error': 'No user input provided'}), 400

        response = voice_assistance(user_input)
        return jsonify({'response': response, 'conversation_history': conversation_history})
    except Exception as e:
        print(f"Error in /process_voice: {e}")
        return jsonify({'error': 'Internal server error'}), 500

# ✅ Run with waitress (production WSGI server)
if __name__ == '__main__':
    print("Running server on http://127.0.0.1:5000")
    serve(app, host='0.0.0.0', port=5000)
