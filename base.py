import requests, os, sys, dotenv, datetime
import PIL.Image
import urllib.request

dotenv.load_dotenv()
API_KEY=os.getenv('API_KEY')

def get_city_weather(city):
    """Get weather data for a city"""
    city = city.lower().strip()
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

ASCII_CHARS = ["@", "#", "$", "%", "?", "*", "+", ";", ":", ",", " "]
ASCII_CHARS.reverse()

def resize(image, new_width = 20):
    width, height = image.size
    new_height = int(new_width * height / width)
    return image.resize((new_width*2, new_height))

def pixel_to_ascii(image):
    pixels = image.getdata()
    ascii_str = "";
    for pixel in pixels:
        ascii_str += ASCII_CHARS[pixel//25];
    return ascii_str

def get_ascii_from_image_url(url):
    """Get ascii art from an image url"""
    urllib.request.urlretrieve(url, "temp.png")
    try:
        image = PIL.Image.open("temp.png")
    except:
        print(url, "Unable to find image ")
    #resize image
    image = resize(image);
    #convert image to greyscale image
    greyscale_image = image.convert("L")
    # convert greyscale image to ascii characters
    ascii_str = pixel_to_ascii(greyscale_image)
    img_width = greyscale_image.width
    ascii_str_len = len(ascii_str)
    ascii_img=""
    #Split the string based on width  of the image
    for i in range(0, ascii_str_len, img_width):
        ascii_img += ascii_str[i:i+img_width] + "\n"
    #save the string to a file
    return ascii_img


def get_weather_forecast(city):
    """Get weather forecast for a city"""
    city = city.lower().strip()
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def get_history(city, date):
    """Get weather history for a city"""
    city = city.lower().strip()
    date = get_unix_timestamp(date)
    url = f'https://history.openweathermap.org/data/2.5/history/city?q={city}&start={date}&cnt=1&appid={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def get_unix_timestamp(date):
    """Get unix timestamp from date"""
    return int(datetime.datetime.strptime(date, '%Y-%m-%d').timestamp())


city = sys.argv[1]
data = get_city_weather(city)
# forecast = get_weather_forecast(city)
# history = get_history(city, "2021-01-01")
ascii = get_ascii_from_image_url(f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}@4x.png")
print(ascii)
print(data)
# print(forecast)
# print(history)
