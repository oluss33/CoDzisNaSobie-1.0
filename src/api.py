import urllib.parse
import urllib.request
import json
from city import City
from weather import Weather

HEADER = {"User-Agent": "CoDzisNaSobie/1.0"}

def fetch_json(url):
    req = urllib.request.Request(url, headers=HEADER)
    return req
def find_city(city):
    founds = []

    safe_city = urllib.parse.quote(city.encode("utf-8"))

    my_url = f"https://geocoding-api.open-meteo.com/v1/search?name={safe_city}&count=5&language=pl&format=json"

    request = fetch_json(my_url)

    try:
        with urllib.request.urlopen(request) as response:
            answer = response.read().decode()
            data = json.loads(answer)

        if "results" not in data or not data["results"]:
            print("brak wynikow")
            return

        print(f"znaleziono dla zapytania {city}:")

        for _city in data["results"]:
            name = _city.get("name")
            country = _city.get("country", "brak")
            lat = _city.get("latitude")
            lon = _city.get("longitude")
            admin1 = _city.get("admin1")

            founds.append(City(name, country, admin1, lat, lon))
            # founds.append((name, country, admin1, lat, lon))

        print(founds)

    except Exception as e:
        print(f"blad {e}")
        return

    return founds

def get_weather(name, latitude, longitude):
    my_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m&forecast_days=1"

    request = fetch_json(my_url)

    with urllib.request.urlopen(request) as response:
        data = json.loads(response.read().decode("utf-8"))

    temperature = data["current"]["temperature_2m"]
    wind = data["current"]["wind_speed_10m"]

    hourly_temp = data["hourly"]["temperature_2m"]

    print(f"POGODA DLA {name.upper()}")
    print(f"tempeartura: {temperature}")
    print(f"wiatr: {wind} km/h")

    return Weather(temperature, wind, hourly_temp)

