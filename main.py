from bot_manager import Messenger
from flask import Flask
from threading import Thread

app = Flask(__name__)

bot = Messenger()
Thread(target=bot.run).start()


@app.route("/")
def home():
    return "Bot is running."

if __name__ == "__main__":
    app.run(port=5000)
