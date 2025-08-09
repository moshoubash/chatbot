from flask import render_template, request, jsonify
from models.chat_model import get_chatbot_response
import markdown

def init_routes(app):
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/chat", methods=["POST"])
    def chat():
        try:
            if not request.json:
                return jsonify({"error": "No JSON data provided"}), 400

            # Get message from the request
            user_input = request.json.get("message")

            # Check if user_input is provided and not empty
            if not user_input:
                return jsonify({"error": "user_input is required"}), 400

            # Get chatbot response and convert markdown to HTML
            response = markdown.markdown(get_chatbot_response(user_input))

            return jsonify({"response": response})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
