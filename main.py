from bot_manager import Messenger
from flask import Flask
from multiprocessing import Process
import requests, os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

messenger = Messenger()
app = Flask(__name__)

# Flask routes
@app.route("/")
def home():
    return "Bot is running with polling."

@app.route("/test-telegram")
def test_telegram():
    token = os.getenv("TOKEN")  # Get your bot token from the environment
    url = f"https://api.telegram.org/bot{token}/getMe"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return f"Telegram API is reachable: {response.json()}", 200
    except requests.exceptions.RequestException as e:
        return f"Error reaching Telegram API: {e}", 500

def run_flask():
    """Run the Flask app."""
    port = int(os.getenv("PORT", 5000))  # Default to port 5000 for local testing
    print(f"Starting Flask app on port {port}...")
    app.run(host="0.0.0.0", port=port)

def run_bot():
    """Run the Telegram bot."""
    print("Starting bot with polling...")
    messenger.run()

if __name__ == "__main__":
    # Run Flask and bot in separate processes
    flask_process = Process(target=run_flask)
    bot_process = Process(target=run_bot)

    flask_process.start()
    bot_process.start()

    flask_process.join()
    bot_process.join()
