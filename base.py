import requests
import os
import sys
import dotenv
import datetime
import PIL.Image
import urllib.request

import style

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
        style.change_color(style.RED)
    elif weather_code in DRIZZLE:
        style.change_color(style.CYAN)
    elif weather_code in RAIN:
        style.change_color(style.BLUE)
    elif weather_code in SNOW:
        style.change_color(style.WHITE)
    elif weather_code in ATMOSPHERE:
        style.change_color(style.BLUE)
    elif weather_code in CLEAR:
        style.change_color(style.YELLOW)
    elif weather_code in CLOUDY:
        style.change_color(style.WHITE)
    else:
        style.change_color(style.RESET)


####################* Printers

def display_weather(data):
    """Display weather (forecast/current) data"""
    if data:
        weather_code = data['weather'][0]['id']
        set_color_on_code(weather_code)
        print(get_ascii_from_image_url(f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}@4x.png"))
        print(f"{'Weather at:':^{style.PADDING}}{data['name']}, {data['sys']['country']}")
        print(f"{'Description:':^{style.PADDING}}{data['weather'][0]['description'].capitalize()}")
        print(f"{'Temp:':^{style.PADDING}}{data['main']['temp']}°C")
        print(f"{'Min/Max Temp:':^{style.PADDING}}{data['main']['temp_min']}°C / {data['main']['temp_max']}°C")
        print(f"{'Feels like:':^{style.PADDING}}{data['main']['feels_like']}°C")
        print(f"{'Humidity:':^{style.PADDING}}{data['main']['humidity']}%")
        print(f"{'Wind:':^{style.PADDING}}{data['wind']['speed']}m/s")
        print(f"{'Pressure:':^{style.PADDING}}{data['main']['pressure']}hPa")
        print(f"{'Visibility:':^{style.PADDING}}{data['visibility']/1000}km")
        print(f"{'Sunrise:':^{style.PADDING}}{datetime.datetime.fromtimestamp(data['sys']['sunrise'])}")
        print(f"{'Sunset:':^{style.PADDING}}{datetime.datetime.fromtimestamp(data['sys']['sunset'])}")
        style.change_color(style.RESET)
    else:
        print("Unable to find city")

def display_history_weather(data):
    """Display (historical) weather data"""
    if data:
        weather_code = data['weather'][0]['id']
        set_color_on_code(weather_code)
        print(get_ascii_from_image_url(f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}@4x.png"))
        print(f"{data['weather'][0]['description']}")
        print(f"{data['main']['temp']}°C")
        print(f"{data['main']['temp_min']}°C / {data['main']['temp_max']}°C")
        print(f"Feels like {data['main']['feels_like']}°C")
        print(f"Humidity {data['main']['humidity']}%")
        print(f"Wind {data['wind']['speed']}m/s")
        print(f"Pressure {data['main']['pressure']}hPa")
        style.change_color(style.RESET)
    else:
        print("Unable to find city")


#####################* Callables

def current_weather(city):
    """Get current weather for a city"""
    data = get_city_weather(city)
    display_weather(data)

def forecast_weather(city):
    """Get weather forecast for a city"""
    data = get_weather_forecast(city)
    display_weather(data["list"][0])

def history_weather(city, date):
    """Get weather history for a city"""
    #! Date format is YYYY-MM-DD
    data = get_history(city, date)
    display_weather(data["list"][0])

city = sys.argv[1]

current_weather(city)
