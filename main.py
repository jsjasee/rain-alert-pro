import telebot
from telebot import TeleBot
from flask import Flask, request
import os

TOKEN = os.getenv("TOKEN")  # Your bot token
WEBHOOK_URL = "https://rain-alert-pro.onrender.com/bot"  # Replace with your Render URL and endpoint

bot = TeleBot(TOKEN)
app = Flask(__name__)

# Handle incoming webhook updates
@app.route("/bot", methods=["POST"])
def webhook():
    # Telegram sends updates as JSON, decode and process them
    json_data = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_data)
    bot.process_new_updates([update])
    return "OK", 200

# Set the webhook when the app starts
if __name__ == "__main__":
    bot.remove_webhook()  # Clear any existing webhook
    bot.set_webhook(url=WEBHOOK_URL)  # Set the new webhook
    app.run(host="0.0.0.0", port=5000)  # Run Flask app
