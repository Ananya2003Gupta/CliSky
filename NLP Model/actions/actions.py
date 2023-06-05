from datetime import datetime
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests


class ActionGetCurrentWeather(Action):
    def name(self) -> Text:
        return "action_get_current_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        location = tracker.get_slot("location")
        api_key = "<openweathermap_api_key>"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"

        response = requests.get(url).json()

        if response["cod"] == "404":
            dispatcher.utter_message(text="Sorry, I couldn't find the weather information for that location.")
        else:
            weather_description = response["weather"][0]["description"]
            temperature = response["main"]["temp"]
            humidity = response["main"]["humidity"]
            wind_speed = response["wind"]["speed"]

            message = f"The current weather in {location} is {weather_description} with a temperature of {temperature}°C. " \
                      f"The humidity is {humidity}% and the wind speed is {wind_speed} m/s."

            dispatcher.utter_message(text=message)

        return []


class ActionGetWeatherForecast(Action):
    def name(self) -> Text:
        return "action_get_weather_forecast"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        location = tracker.get_slot("location")
        api_key = "<openweathermap_api_key>"
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}&units=metric"

        response = requests.get(url).json()

        if response["cod"] == "404":
            dispatcher.utter_message(text="Sorry, I couldn't find the weather forecast for that location.")
        else:
            forecast_list = response["list"]

            message = f"The weather forecast for {location} is as follows:\n"

            for forecast in forecast_list:
                forecast_datetime = datetime.fromtimestamp(forecast["dt"])
                forecast_date = forecast_datetime.strftime("%Y-%m-%d")
                forecast_time = forecast_datetime.strftime("%H:%M:%S")
                weather_description = forecast["weather"][0]["description"]
                temperature = forecast["main"]["temp"]

                message += f"- Date: {forecast_date}, Time: {forecast_time}, Weather: {weather_description}, " \
                           f"Temperature: {temperature}°C\n"

            dispatcher.utter_message(text=message)

        return []


class ActionGetHistoricalWeatherForecast(Action):
    def name(self) -> Text:
        return "action_get_historical_weather_forecast"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        location = tracker.get_slot("location")
        date = tracker.get_slot("date")

        # Perform the necessary operations to retrieve historical weather forecast information
        # based on the location and date, using your preferred data source or API.

        message = f"The historical weather forecast for {location} on {date} is as follows: <insert details>"
        dispatcher.utter_message(text=message)
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
