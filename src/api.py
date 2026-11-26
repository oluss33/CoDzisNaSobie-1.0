import urllib.parse
import urllib.request
import json
from city import City
from weather import Weather
import datetime

HEADER = {"User-Agent": "CoDzisNaSobie/1.0"}

def build_request(url):
    req = urllib.request.Request(url, headers=HEADER)
    return req
def find_city(city, page):
    founds = []

    safe_city = urllib.parse.quote(city.encode("utf-8"))

    my_url = f"https://geocoding-api.open-meteo.com/v1/search?name={safe_city}&count=5&language=pl&format=json"

    request = build_request(my_url)

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

            founds.append(City(page, name, country, admin1, lat, lon))

        print(founds)

    except Exception as e:
        print(f"blad {e}")
        return

    return founds

def get_weather(name, latitude, longitude):
    my_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m,pressure_msl,weather_code&hourly=temperature_2m,pressure_msl,precipitation,precipitation_probability,snowfall,rain&timezone=auto&forecast_days=1"

    request = build_request(my_url)

    with urllib.request.urlopen(request, timeout=45) as response:
        data = json.loads(response.read().decode("utf-8"))

    temperature = data["current"]["temperature_2m"]
    wind = data["current"]["wind_speed_10m"]
    pressure = data["current"]["pressure_msl"]
    weather_code = data["current"]["weather_code"]

    hourly_temp = data["hourly"]["temperature_2m"]
    hourly_pressure = data["hourly"]["pressure_msl"]
    precipitation = data["hourly"]["precipitation"]
    precipitation_propability = data["hourly"]["precipitation_probability"]
    snowfall = data["hourly"]["snowfall"]
    rain = data["hourly"]["rain"]

    current_hour = int(data["current"]["time"][11:13])  # godzina w API, wzgledem lat i lon, 11-12 wlacznie pozycja godizny

    print(f"POGODA DLA {name.upper()}")
    print(f"tempeartura: {temperature}")
    print(f"wiatr: {wind} km/h")
    print(f"snieg: {snowfall}")
    print(f"deszcz: {rain}")

    return Weather(temperature, wind, pressure, hourly_temp, hourly_pressure, precipitation, precipitation_propability, snowfall, rain, weather_code, current_hour)

def translate_weather_code(code):
    code = str(code)
    codes_dict = {
        "0": "Bezchmurnie",
        "1": "Przeważnie bezchmurnie",
        "2": "Częściowe zachmurzenie",
        "3": "Pochmurno",
        "45": "Mgła",
        "48": "Mgła osadzająca szadź",
        "51": "Lekka mżawka",
        "53": "Umiarkowana mżawka",
        "55": "Gęsta mżawka",
        "56": "Lekka marznąca mżawka",
        "57": "Gęsta marznąca mżawka",
        "61": "Lekki deszcz",
        "63": "Umiarkowany deszcz",
        "65": "Silny deszcz",
        "66": "Lekki marznący deszcz",
        "67": "Silny marznący deszcz",
        "71": "Lekkie opady śniegu",
        "73": "Umiarkowane opady śniegu",
        "75": "Intensywne opady śniegu",
        "77": "Śnieg ziarnisty",
        "80": "Lekkie przelotne opady deszczu",
        "81": "Umiarkowane przelotne opady deszczu",
        "82": "Gwałtowne przelotne opady deszczu",
        "85": "Lekkie przelotne opady śniegu",
        "86": "Intensywne przelotne opady śniegu",
        "95": "Burza",
        "96": "Burza z lekkim gradem",
        "97": "Silna burza",
        "99": "Burza z silnym gradem"
    }

    return codes_dict.get(code, "Nieznany kod pogody")