import requests
import datetime as dt
import os
from dotenv import load_dotenv

load_dotenv() # this must be called before using os.getenv()
API_KEY = os.getenv("API_KEY")
LAT = os.getenv("LAT")
LONG = os.getenv("LONG")

def add_emojis(message):
    possible_weather_conditions = {
        "cloudy": "⛅",
        "overcast": "☁️",
        "rain": "🌧️",
        "thunder": "⚡️",
        "storm": "⛈️",
    }
    for weather in possible_weather_conditions:
        if weather in message.lower():
            message += possible_weather_conditions[weather]
    return message

class ApiManager:
    def __init__(self):

        self.params = {
            "key": API_KEY,
            "include": "",
        }

        self.current_time = dt.datetime.now()
        self.chosen_time_formatted = ""

        self.api_endpoint = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{LAT},{LONG}/{self.chosen_time_formatted}"

        self.data = self.get_data()

    def get_data(self):
        """Updates the data again."""
        response = requests.get(
            url=self.api_endpoint,
            params=self.params)
        response.raise_for_status()
        self.data = response.json()
        return response.json()

    def get_rain_prob_data(self):
        self.current_time = dt.datetime.now()
        self.get_data()
        all_days = self.data["days"]
        current_day = all_days[0]
        try:
            hours_today = current_day["hours"]
        except KeyError:
            return "There seems to be a problem gathering weather data. Try again later."

        else:
            precip_prob = [hour_dict["precipprob"] for hour_dict in hours_today if self.current_time.hour == int(hour_dict["datetime"].split(":")[0]) or self.current_time.hour + 1 == int(hour_dict["datetime"].split(":")[0]) or self.current_time.hour + 2 == int(hour_dict["datetime"].split(":")[0])]
            # print(precip_prob)
            mean_precip_prob = round(sum(precip_prob) / len(precip_prob), 1)
            if mean_precip_prob > 80:
                return f"🔴 It is highly likely to rain now and in the next 2 hours. Precip prob: {mean_precip_prob} %"
            elif 50 <= mean_precip_prob < 80:
                return f"🟡 It is likely to rain now and in the next 2 hours. Precip prob: {mean_precip_prob} %"
            else:
                return f"🟢 It is unlikely to rain now and in the next 2 hours. Precip prob: {mean_precip_prob} %"

    def get_daily_forecast_data(self):
        self.get_data()
        condition_today = self.data["days"][0]["conditions"]
        desc_today = self.data["days"][0]["description"]
        return f"Today's weather: {add_emojis(condition_today)}. {add_emojis(desc_today)}"

    def get_hourly_forecast_data(self):
        self.get_data()
        hrly_weather_tdy_list = self.data["days"][0]["hours"]
        messages = [f"{hour['datetime']}: {hour['conditions']}" for hour in hrly_weather_tdy_list]
        emoji_messages = [add_emojis(message) for message in messages]
        message_result = "\n".join(emoji_messages)
        return message_result

    def get_chosen_date_data(self, user_input_date):
        """only works for a 15 day period starting from current date. user_input_date must follow the format YYYY-MM-DD"""
        self.chosen_time_formatted = user_input_date
        self.get_data()

        for day in self.data['days']:
            if day['datetime'] == user_input_date:
                messages = [f"{hour['datetime']}: {hour['conditions']}" for hour in day['hours']]
                emoji_messages = [add_emojis(message) for message in messages]
                message_result = "\n".join(emoji_messages)
                overall_result = f"Overall condition: {add_emojis(day['conditions'])}\nDescription: {add_emojis(day['description'])}\n"
                return overall_result + message_result
        return ("No match found. Date must be within 15 day period starting from today. "
                "Try re-entering date using the specified format of YYYY-MM-DD")

    def get_15_days_data(self):
        self.params["include"] = "days"
        self.get_data()
        message = [f"{add_emojis(day['datetime'])}: {add_emojis(day['conditions'])}. {add_emojis(day['description'])}" for day in self.data['days']]
        result = "\n".join(message)
        return result

api_manager = ApiManager()
print(api_manager.get_rain_prob_data())