import pytz
import requests
import datetime as dt
import os
from dotenv import load_dotenv

load_dotenv() # this must be called before using os.getenv()
API_KEY = os.getenv("API_KEY")
LAT = os.getenv("LAT")
LONG = os.getenv("LONG")
SINGAPORE_TZ = pytz.timezone("Asia/Singapore")

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
            "include": [],
        }

        self.current_time = dt.datetime.now(SINGAPORE_TZ)
        self.chosen_time_formatted = str(self.current_time).split(" ")[0] + "T" + str(self.current_time.hour) + ":00:00"

        self.api_endpoint = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{LAT},{LONG}"

        self.data = self.get_data()

    def reset_params(self):
        self.params['include'] = []

    def get_data(self):
        """Updates the data again."""
        self.current_time = dt.datetime.now(SINGAPORE_TZ) # updates the current time
        response = requests.get(
            url=self.api_endpoint,
            params=self.params)
        response.raise_for_status()
        self.data = response.json()
        return response.json()

    def get_rain_prob_data(self):
        self.reset_params()  # IF PREVIOUS FUNCTIONS WERE CALLED WHICH REQUIRED MODIFICATION OF PARAMS eg. checking daily weather, this resets the CURRENT params!
        self.api_endpoint += f"/{self.chosen_time_formatted}"
        self.get_data()
        self.api_endpoint = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{LAT},{LONG}"
        current_day = self.data["days"][0]
        try:
            hours_today = current_day['hours']
        except KeyError:
            return "There seems to be a problem gathering weather data. Try resetting the params using /reset_params."

        else:
            list_of_hours = [self.current_time.hour, self.current_time.hour+1, self.current_time.hour+2]
            precip_prob = []
            for hour_dict in hours_today:
                for hour in list_of_hours:
                    if int(hour_dict["datetime"].split(":")[0]) == hour:
                        precip_prob.append(hour_dict["precipprob"])

            # precip_prob = [hour_dict["precipprob"] for hour_dict in hours_today if self.current_time.hour == int(hour_dict["datetime"].split(":")[0]) or self.current_time.hour + 1 == int(hour_dict["datetime"].split(":")[0]) or self.current_time.hour + 2 == int(hour_dict["datetime"].split(":")[0])]
            print(precip_prob)
            mean_precip_prob = round(sum(precip_prob) / len(precip_prob), 1)
            print(mean_precip_prob)
            if mean_precip_prob > 80:
                return f"🔴 It is highly likely to rain now and in the next 2 hours. Precip prob: {mean_precip_prob} %.\nPrecip prob for next 2 hrs: {precip_prob}. Hours searched: {list_of_hours} on {self.data['days'][0]['datetime']} "
            elif 50 <= mean_precip_prob < 80:
                return f"🟡 It is likely to rain now and in the next 2 hours. Precip prob: {mean_precip_prob} %.\nPrecip prob for next 2 hrs: {precip_prob}. Hours searched: {list_of_hours} on {self.data['days'][0]['datetime']} "
            else:
                return f"🟢 It is unlikely to rain now and in the next 2 hours. Precip prob: {mean_precip_prob} %.\nPrecip prob for next 2 hrs: {precip_prob}. Hours searched: {list_of_hours} on {self.data['days'][0]['datetime']} "

    def get_daily_forecast_data(self):
        self.reset_params()
        self.get_data()
        condition_today = self.data["days"][0]["conditions"]
        desc_today = self.data["days"][0]["description"]
        return f"Today's weather: {add_emojis(condition_today)}. {add_emojis(desc_today)}"

    def get_hourly_forecast_data(self):
        self.reset_params()
        self.get_data()
        try:
            hrly_weather_tdy_list = self.data["days"][0]["hours"]
        except KeyError:
            return "There seems to be a problem gathering hourly data. Please try again later."
        else:
            messages = [f"{hour['datetime']}: {hour['conditions']}" for hour in hrly_weather_tdy_list]
            emoji_messages = [add_emojis(message) for message in messages]
            message_result = "\n".join(emoji_messages)
            return message_result

    def get_chosen_date_data(self, user_input_date):
        """only works for a 15 day period starting from current date. user_input_date must follow the format YYYY-MM-DD"""
        self.reset_params()
        self.chosen_time_formatted = user_input_date
        self.get_data()

        for day in self.data['days']:
            if day['datetime'] == user_input_date:
                try:
                    messages = [f"{hour['datetime']}: {hour['conditions']}" for hour in day['hours']]
                except KeyError:
                    return "There seems to be a problem gathering hourly data. Please try again later."
                else:
                    emoji_messages = [add_emojis(message) for message in messages]
                    message_result = "\n".join(emoji_messages)
                    overall_result = f"Overall condition: {add_emojis(day['conditions'])}\nDescription: {add_emojis(day['description'])}\n"
                    return overall_result + message_result
        return ("No match found. Date must be within 15 day period starting from today. "
                "Try re-entering date using the specified format of YYYY-MM-DD")

    def get_15_days_data(self):
        self.params["include"] = ["days"]
        self.get_data()
        message = [f"{add_emojis(day['datetime'])}: {add_emojis(day['conditions'])}. {add_emojis(day['description'])}" for day in self.data['days']]
        result = "\n".join(message)
        self.reset_params()
        return result

# api_manager = ApiManager()