import requests
import os
import sys
import dotenv
import datetime
import PIL.Image
import urllib.request

from .style import *

dotenv.load_dotenv()
API_KEY = os.getenv('API_KEY')

ASCII_CHARS = ["@", "#", "$", "%", "?", "*", "+", ";", ":", ",", " "]
ASCII_CHARS.reverse()


######################? API Calls

def get_city_weather(city):
    """Get weather data for a city"""
    city = city.lower().strip()
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_weather_forecast(city):
    """Get weather forecast for a city"""
    city = city.lower().strip()
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&cnt=1&appid={API_KEY}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_history(city, date):
    """Get weather history for a city"""
    city = city.lower().strip()
    date = get_unix_timestamp(date)
    url = f'https://history.openweathermap.org/data/2.5/history/city?q={city}&start={date}&cnt=1&appid={API_KEY}&units=metric'
    response = requests.get(url)
    print(response.text)
    if response.status_code == 200:
        return response.json()
    else:
        return None

######################? Helpers

def resize(image, new_width=20):
    width, height = image.size
    new_height = int(new_width * height / width)
    return image.resize((new_width*2, new_height))


def pixel_to_ascii(image):
    pixels = image.getdata()
    ascii_str = ""
    for pixel in pixels:
        ascii_str += ASCII_CHARS[pixel//25]
    return ascii_str


def get_ascii_from_image_url(url):
    """Get ascii art from an image url"""
    urllib.request.urlretrieve(url, "temp.png")
    try:
        image = PIL.Image.open("temp.png")
    except:
        print(url, "Unable to find image ")
    # resize image
    image = resize(image)
    # convert image to greyscale image
    greyscale_image = image.convert("L")
    # convert greyscale image to ascii characters
    ascii_str = pixel_to_ascii(greyscale_image)
    img_width = greyscale_image.width
    ascii_str_len = len(ascii_str)
    ascii_img = ""
    # Split the string based on width  of the image
    for i in range(0, ascii_str_len, img_width):
        ascii_img += ascii_str[i:i+img_width] + "\n"
    # save the string to a file
    return ascii_img

def get_unix_timestamp(date):
    """Get unix timestamp from date"""
    return int(datetime.datetime.strptime(date, '%Y-%m-%d').timestamp())


def set_color_on_code(weather_code):
    """Set color for terminal"""
    THUNDERSTORM = range(200, 300)
    DRIZZLE = range(300, 400)
    RAIN = range(500, 600)
    SNOW = range(600, 700)
    ATMOSPHERE = range(700, 800)
    CLEAR = range(800, 801)
    CLOUDY = range(801, 900)
    if weather_code in THUNDERSTORM:
        return change_color(RED)
    elif weather_code in DRIZZLE:
        return change_color(CYAN)
    elif weather_code in RAIN:
        return change_color(BLUE)
    elif weather_code in SNOW:
        return change_color(WHITE)
    elif weather_code in ATMOSPHERE:
        return change_color(BLUE)
    elif weather_code in CLEAR:
        return change_color(YELLOW)
    elif weather_code in CLOUDY:
        return change_color(WHITE)
    else:
        return change_color(RESET)


####################* Printers

def display_weather(data):
    """Display weather (forecast/current) data"""
    s = ""
    if data:
        weather_code = data['weather'][0]['id']
        s += set_color_on_code(weather_code)
        s += (get_ascii_from_image_url(f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}@4x.png"))
        s += (f"{'Weather at:':^{PADDING}}{data['name']}, {data['sys']['country']}\n")
        s += (f"{'Description:':^{PADDING}}{data['weather'][0]['description'].capitalize()}\n")
        s += (f"{'Temp:':^{PADDING}}{data['main']['temp']}°C\n")
        s += (f"{'Min/Max Temp:':^{PADDING}}{data['main']['temp_min']}°C / {data['main']['temp_max']}°C\n")
        s += (f"{'Feels like:':^{PADDING}}{data['main']['feels_like']}°C\n")
        s += (f"{'Humidity:':^{PADDING}}{data['main']['humidity']}%\n")
        s += (f"{'Wind:':^{PADDING}}{data['wind']['speed']}m/s\n")
        s += (f"{'Pressure:':^{PADDING}}{data['main']['pressure']}hPa\n")
        s += (f"{'Visibility:':^{PADDING}}{data['visibility']/1000}km\n")
        s += (f"{'Sunrise:':^{PADDING}}{datetime.datetime.fromtimestamp(data['sys']['sunrise'])}\n")
        s += (f"{'Sunset:':^{PADDING}}{datetime.datetime.fromtimestamp(data['sys']['sunset'])}\n")
        s += change_color(RESET)
    else:
        s += ("Unable to find city")
    return s

def display_forecast_weather(data):
    """Display weather (forecast/current) data"""
    s = ""
    if data:
        weather_code = data['list'][0]['weather'][0]['id']
        s += set_color_on_code(weather_code)
        s += (get_ascii_from_image_url(f"https://openweathermap.org/img/wn/{data['list'][0]['weather'][0]['icon']}@4x.png"))
        s += (f"{'Weather at:':^{PADDING}}{data['city']['name']}, {data['city']['country']}\n")
        s += (f"{'Description:':^{PADDING}}{data['list'][0]['weather'][0]['description'].capitalize()}\n")
        s += (f"{'Temp:':^{PADDING}}{data['list'][0]['main']['temp']}°C\n")
        s += (f"{'Min/Max Temp:':^{PADDING}}{data['list'][0]['main']['temp_min']}°C / {data['list'][0]['main']['temp_max']}°C\n")
        s += (f"{'Feels like:':^{PADDING}}{data['list'][0]['main']['feels_like']}°C\n")
        s += (f"{'Humidity:':^{PADDING}}{data['list'][0]['main']['humidity']}%\n")
        s += (f"{'Wind:':^{PADDING}}{data['list'][0]['wind']['speed']}m/s\n")
        s += (f"{'Pressure:':^{PADDING}}{data['list'][0]['main']['pressure']}hPa\n")
        s += (f"{'Visibility:':^{PADDING}}{data['list'][0]['visibility']/1000}km\n")
        s += (f"{'Sunrise:':^{PADDING}}{datetime.datetime.fromtimestamp(data['city']['sunrise'])}\n")
        s += (f"{'Sunset:':^{PADDING}}{datetime.datetime.fromtimestamp(data['city']['sunset'])}\n")
        s += change_color(RESET)
    else:
        s += ("Unable to find city")
    return s

def display_history_weather(data):
    """Display (historical) weather data"""
    s = ""
    if data:
        weather_code = data['weather'][0]['id']
        s += set_color_on_code(weather_code)
        s += (get_ascii_from_image_url(f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}@4x.png"))
        s += (f"{data['weather'][0]['description']}\n")
        s += (f"{data['main']['temp']}°C\n")
        s += (f"{data['main']['temp_min']}°C / {data['main']['temp_max']}°C\n")
        s += (f"Feels like {data['main']['feels_like']}°C\n")
        s += (f"Humidity {data['main']['humidity']}%\n")
        s += (f"Wind {data['wind']['speed']}m/s\n")
        s += (f"Pressure {data['main']['pressure']}hPa\n")
        s += change_color(RESET)
    else:
        s += ("Unable to find city")
    return s


#####################* Callables

def current_weather(city):
    """Get current weather for a city"""
    data = get_city_weather(city)
    return display_weather(data)

def forecast_weather(city):
    """Get weather forecast for a city"""
    data = get_weather_forecast(city)
    return display_forecast_weather(data)

def history_weather(city, date):
    """Get weather history for a city"""
    #! Date format is YYYY-MM-DD
    data = get_history(city, date)
    return display_weather(data["list"][0])

