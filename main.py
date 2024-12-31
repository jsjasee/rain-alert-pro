from bot_manager import Messenger
from flask import Flask
from threading import Thread

messenger = Messenger()
app = Flask(__name__)

# Optional root route for confirmation
@app.route("/")
def home():
    return "Bot is running with polling."

# Start the bot with polling
if __name__ == "__main__":
    print("Starting bot with polling...")
    Thread(target=lambda: messenger.bot.polling(non_stop=True)).start()
    # Start Flask app to satisfy Render's port requirement
    app.run(host="0.0.0.0", port=5000)