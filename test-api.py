import urllib.parse
import urllib.request
import json

def szukaj(city):

    founds = []

    safe_city = urllib.parse.quote(city.encode("utf-8"))

    my_url = f"https://geocoding-api.open-meteo.com/v1/search?name={safe_city}&count=5&language=pl&format=json"

    header = {"User-Agent": "CoDzisNaSobie/1.0"}
    req = urllib.request.Request(my_url, headers=header)

    try:
        with urllib.request.urlopen(req) as response:
            answer = response.read().decode()
            data = json.loads(answer)

        if "results" not in data or not data["results"]:
            print("brak wynikow")
            return

        print(f"znaleziono dla zapytania {city.upper()}:")

        for _city in data["results"]:
            name = _city.get("name")
            country = _city.get("country", "brak")
            lat = _city.get("latitude")
            lon = _city.get("longitude")
            admin1 = _city.get("admin1")


            founds.append((name, country, admin1, lat, lon))

        print(founds)

    except Exception as e:
        print(f"blad {e}")
        return

    return founds

def get_weather(name, latitude, longitude):
    my_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m"
    header = {"User-Agent": "CoDzisNaSobie/1.0"}
    req = urllib.request.Request(my_url, headers=header)

    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode("utf-8"))

    temperature = data["current"]["temperature_2m"]
    wind = data["current"]["wind_speed_10m"]

    print(f"POGODA DLA {name.upper()}")
    print(f"tempeartura: {temperature}")
    print(f"wiatr: {wind} km/h")

miasto = input("miasto: ")
city_list = szukaj(miasto)

choice = int(input("wybierz id miasta: "))

my_city = city_list[choice]
get_weather(my_city[0], my_city[3], my_city[4])

