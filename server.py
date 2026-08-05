"""
PromptGuard REST API.

Provides endpoints for prompt analysis,
health monitoring and project information.

"""


from flask import Flask, request, jsonify
from engines import analyzer

app = Flask(__name__)


@app.route("/")
def home():
    return {
        "message": "Semantic Search Engine API is running!"
    }

@app.route("/analyze" , methods = ["POST"])
def analyze():

    data = request.get_json()

    if data is None:
        return jsonify({
            "error": "Request body must be valid JSON."
        }), 400

    if "prompt" not in data:
        return jsonify({
            "error": "Missing required field: 'prompt'."
        }), 400

    prompt = data["prompt"]

    if not isinstance(prompt, str):
        return jsonify({
            "error": "Prompt must be a string."
        }), 400

    prompt = prompt.strip()

    if not prompt:
        return jsonify({
            "error": "Prompt cannot be empty."
        }), 400


    prompt = data["prompt"]

    results = analyzer.analyze_prompt(prompt)

    return jsonify({
    "prompt": prompt,
    **results
})

@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "healthy",
        "service": "PromptGuard",
        "version": "1.0.0"
    }), 200


@app.route("/about", methods=["GET"])
def about():

    return jsonify({
        "project": "PromptGuard",
        "description": "Hybrid AI Prompt Injection Detection Engine",
        "version": "1.0.0",
        "engines": [
            "Rule Engine",
            "Semantic Engine",
            "Machine Learning Engine"
        ]
    }), 200

if __name__ == "__main__":
    app.run(debug=True)