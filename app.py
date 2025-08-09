from flask import Flask
from controllers.chat_controller import init_routes
import os

app = Flask(__name__)
init_routes(app)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)