from bot_manager import Messenger

messenger = Messenger()

# Start the bot with polling
if __name__ == "__main__":
    print("Starting bot with polling...")
    messenger.bot.polling(non_stop=True)