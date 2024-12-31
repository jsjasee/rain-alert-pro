import telebot
from bot_manager import Messenger
from flask import Flask, request

WEBHOOK_URL = "https://rain-alert-pro.onrender.com/bot"  # Replace with your Render URL and endpoint

messenger = Messenger()
app = Flask(__name__)

# Handle incoming webhook updates
@app.route("/bot", methods=["POST"])
def webhook():
    # Telegram sends updates as JSON, decode and process them
    json_data = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_data)
    messenger.bot.process_new_updates([update])
    return "OK", 200

# Add a route for the root URL
@app.route("/")
def home():
    return "Welcome to the Rain Alert Bot! This bot uses webhooks to receive updates. Rain Alert Bot executed successfully."

# Set the webhook when the app starts
if __name__ == "__main__":
    messenger.bot.remove_webhook()  # Clear any existing webhook
    messenger.bot.set_webhook(url=WEBHOOK_URL)  # Set the new webhook
    app.run(host="0.0.0.0", port=5000)  # Run Flask app
