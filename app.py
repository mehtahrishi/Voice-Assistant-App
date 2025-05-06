from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

OPENROUTER_API_KEY = "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"  # Replace this

def query_openrouter(prompt):
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",  # You can change to your domain if deployed
        }
        data = {
            "model": "mistralai/mistral-7b-instruct",  # Free, reliable
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("OpenRouter error:", e)
        return "Sorry, I couldn't think of anything to say!"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_input = data.get("user_input", "").strip()

    if not user_input:
        return jsonify({"response": "Sorry, I didn't catch that."})

    # Rule-based responses
    lowered = user_input.lower()
    if "hello" in lowered:
        response = "Hi! How can I help you?"
    elif "your name" in lowered:
        response = "I’m Nami voice assistant!"
    elif "time" in lowered:
        # Include both time and date in the response
        response = "The current time is " + datetime.now().strftime("%H:%M") + " on " + datetime.now().strftime("%A, %B %d, %Y")
    elif "how are you" in lowered:
        response = "I'm just code, but feeling quite functional!"
    elif "bye" in lowered:
        response = "Goodbye! Have a great day!"
    else:
        # Fallback to OpenRouter
        response = query_openrouter(user_input)

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
