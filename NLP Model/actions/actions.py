import re
from datetime import datetime
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
from .base import *


def extract_city_name(text):
    # Use regex pattern to extract city name from user input
    pattern = r"\[(.*?)\]\(city\)"
    matches = re.findall(pattern, text)
    if matches:
        return matches[0]
    else:
        return None


class ActionGetCurrentWeather(Action):
    def name(self):
        return "action_get_current_weather"

    def extract_city_name(text):
        # Use regex pattern to extract city name from user input
        pattern = r"\[(.*?)\]\(city\)"
        matches = re.findall(pattern, text)
        if matches:
            return matches[0]
        else:
            return None

    def run(self, dispatcher, tracker, domain):
        # Extract necessary slots from the tracker
        city = next(tracker.get_latest_entity_values("city"), None)

        # Extract city name from user input using regex
        # city = user_message

        if not city:
            response_text = "I couldn't detect the city in your input. Please provide a valid city name."
            dispatcher.utter_message(response_text)
            return []

        # # Make the API request to fetch current weather data
        # api_key = "OPENWEATHERMAP_API_KEY"
        # url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        # response = requests.get(url)
        # data = response.json()

        # if "main" in data and "temp" in data["main"] and "weather" in data:
        #     temperature = data["main"]["temp"]
        #     weather_description = data["weather"][0]["description"]
        #     response_text = f"The current weather in {city} is {temperature}°C with {weather_description}."
        # else:
        #     response_text = "I couldn't retrieve the current weather data for the specified location."

        # # Send the response back to the user
        # dispatcher.utter_message(response_text)
        dispatcher.utter_message(current_weather(city))

        return []


class ActionGetWeatherForecast(Action):
    def name(self):
        return "action_get_weather_forecast"

    def extract_city_name(text):
        # Use regex pattern to extract city name from user input
        pattern = r"\[(.*?)\]\(city\)"
        matches = re.findall(pattern, text)
        if matches:
            return matches[0]
        else:
            return None

    def run(self, dispatcher, tracker, domain):
        # Extract necessary slots from the tracker
        city = next(tracker.get_latest_entity_values("city"), None)


        if not city:
            response_text = "I couldn't detect the city in your input. Please provide a valid city name."
            dispatcher.utter_message(response_text)
            return []

        # Make the API request to fetch weather forecast data
        # api_key = "OPENWEATHERMAP_API_KEY"
        # url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}"
        # response = requests.get(url)
        # data = response.json()

        # forecasts = data.get("list", [])
        # if forecasts:
        #     response_text = f"Here is the weather forecast for {city}:\n"
        #     for forecast in forecasts:
        #         temperature = forecast["main"]["temp"]
        #         weather_description = forecast["weather"][0]["description"]
        #         response_text += f"- Temperature: {temperature}°C, Weather: {weather_description}\n"
        # else:
        #     response_text = "I couldn't retrieve the weather forecast for the specified location."

        # # Send the response back to the user
        # dispatcher.utter_message(response_text)
        dispatcher.utter_message(forecast_weather(city))

        return []


class ActionGetHistoricalWeatherForecast(Action):
    def name(self):
        return "action_get_historical_weather_forecast"

    def extract_city_name(text):
        # Use regex pattern to extract city name from user input
        pattern = r"\[(.*?)\]\(city\)"
        matches = re.findall(pattern, text)
        if matches:
            return matches[0]
        else:
            return None

    def run(self, dispatcher, tracker, domain):
        # Extract necessary slots from the tracker
        city = next(tracker.get_latest_entity_values("city"), None)
        date = next(tracker.get_latest_entity_values("date"), None)


        if not city:
            response_text = "I couldn't detect the city in your input. Please provide a valid city name."
            dispatcher.utter_message(response_text)
            return []

        # # Convert the date to the required format for the API request
        # formatted_date = datetime.datetime.strptime(date, "%M %d %Y").strftime("%Y-%m-%d")

        # # Make the API request to fetch historical weather data
        # api_key = "OPENWEATHERMAP_API_KEY"
        # url = f"http://api.openweathermap.org/data/2.5/onecall/timemachine?lat={location['latitude']}&lon={location['longitude']}&dt={formatted_date}&appid={api_key}"
        # response = requests.get(url)
        # data = response.json()

        # # Make the API request to fetch historical weather data
        # api_key = "OPENWEATHERMAP_API_KEY"
        # url = f"http://api.openweathermap.org/data/2.5/onecall/timemachine?q={city}&dt={formatted_date}&appid={api_key}"
        # response = requests.get(url)
        # data = response.json()

        # if "current" in data and "temp" in data["current"] and "weather" in data["current"]:
        #     temperature = data["current"]["temp"]
        #     weather_description = data["current"]["weather"][0]["description"]
        #     response_text = f"The historical weather on {date} in {city} was {temperature}°C with {weather_description}."
        # else:
        #     response_text = "I couldn't retrieve the historical weather data for the specified location and date."

        # # Send the response back to the user
        # dispatcher.utter_message(response_text)
        dispatcher.utter_message(history_weather(city, date))
        return []


class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="I'm sorry, but I didn't understand your question. "
                                      "Please rephrase or try a different query.")

        return []
