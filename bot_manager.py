from telebot import TeleBot
from api_manager import ApiManager
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

api_manager = ApiManager()

class Messenger:
    def __init__(self):
        self.bot = TeleBot(token=TOKEN)
        self.user_states = {}

        self.bot.message_handler(commands=['start'])(self.say_hello)
        self.bot.message_handler(commands=['will_it_rain'])(self.will_it_rain)
        self.bot.message_handler(commands=['daily_forecast'])(self.daily_forecast)
        self.bot.message_handler(commands=['hourly_forecast'])(self.hourly_forecast)
        self.bot.message_handler(commands=['specified_forecast'])(self.specified_forecast)
        self.bot.message_handler(func=self.check_condition)(self.send_specified_forecast)
        self.bot.message_handler(commands=['fifteen_days_forecast'])(self.fifteen_days_forecast)
        self.bot.polling()

    def send_message(self, msg):
        self.bot.send_message(chat_id=msg.chat.id, text=msg)

    def say_hello(self, message):
        # Key Takeaway
        # The message argument is required because Telebot always passes the incoming message object to the handler.
        # Even if you don’t use it, you must include it in the
        # function’s signature (aka the number of parameters the function accepts)
        # to match what Telebot expects. You can safely ignore it with _ if it’s not needed.

        # The message_handler Decorator: When you use @bot.message_handler, Telebot automatically calls the associated function whenever a message matches the specified condition (like /start).
        # The message Parameter: Telebot always passes the message object as an argument to the handler function.
        # This message object contains information about the incoming message, such as the text, chat ID, and sender details.
        # the chat is an object in the object, and you tap into the id attribute of chat to get the user_id
        self.bot.send_message(chat_id=message.chat.id, text="Please click on the menu to see what I can do!")

    def will_it_rain(self, message):
        weather_forecast = api_manager.get_rain_prob_data()
        self.bot.send_message(chat_id=message.chat.id, text=weather_forecast)

    def daily_forecast(self, message):
        weather_forecast = api_manager.get_daily_forecast_data()
        self.bot.send_message(chat_id=message.chat.id, text=weather_forecast)

    def hourly_forecast(self, message):
        weather_forecast = api_manager.get_hourly_forecast_data()
        self.bot.send_message(chat_id=message.chat.id, text=weather_forecast)

    def specified_forecast(self, message):
        self.bot.send_message(chat_id=message.chat.id, text="The date entered must be within a 15 day period, starting from today. "
                                                    "Please enter a date with the FORMAT YYYY-MM-DD")
        self.user_states[message.chat.id] = "waiting_for_date"

    def check_condition(self, message):
        if message.chat.id in self.user_states and self.user_states[message.chat.id] == "waiting_for_date":
            return True
        else:
            return False

    def send_specified_forecast(self, message):
        # the message is an object passed in by telebot with attributes we can tap into
        user_date = message.text
        result = api_manager.get_chosen_date_data(user_date)
        self.bot.send_message(chat_id=message.chat.id, text=result)
        self.user_states = {}

    def fifteen_days_forecast(self, message):
        result = api_manager.get_15_days_data()
        self.bot.send_message(chat_id=message.chat.id, text=result)