from bot_manager import Messenger
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    bot = Messenger()
    return "Bot is running."

if __name__ == "__main__":
    app.run(port=5000)
