import json
import os

FILE_PATH = "data/data.json"

activities_dict = {
            "Bieganie": "running",
            "Wrażliwość na zimno": "cold",
            "Odporność na zimno": "cold_resistance",
            "Częste spacery": "often_walking",
            "Trening siłowy": "gym",
            "Rzadkie wyjścia z domu": "rarely_outside",
            "Wrażliwość na wysokie ciśnienie": "pressure_sensitive",
            "Jazda na rowerze": "cycling",
            "Wrażliwość na wiatr": "wind_sensitive",
            "Częste przeziębienia": "often_sick"
        }

def load_json():

    if not os.path.exists(FILE_PATH):
        return { }
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as my_file:
            return json.load(my_file)
    except:
        return { }

def save_json(data):
    with open(FILE_PATH, "w", encoding="utf-8") as my_file:
        json.dump(data, my_file, indent=4, ensure_ascii=True)

def save_user_activities(user_id, active_activities : list):
    print("zapisuje uesr activitiy")
    data = load_json()

    if str(user_id) not in data.keys():
        data[str(user_id)] = {}

    data[str(user_id)]["active_activities"] = active_activities

    save_json(data)

def get_fav_cities(user_id):

    if user_id is None:
        return {}

    data = load_json()

    if str(user_id) not in data.keys():
        return {}

    info = data[str(user_id)].get("cities", {})

    return info

def is_city_favorite(user_id, name):
    data = load_json()

    user_info = data.get(str(user_id), {})
    fav_cities = user_info.get("cities", {})

    if name not in fav_cities.keys():
        return False
    return True

def add_city(user_id, name, lat, lon, country, admin):
    data = load_json()
    if str(user_id) not in data.keys():
        data[str(user_id)] = { }

    user_info = data[str(user_id)]

    if "cities" not in user_info.keys():
        user_info["cities"] = {}

    user_info["cities"][name] = [lon, lat, country, admin]

    save_json(data)

def remove_city(user_id, name):
    data = load_json()

    user_info = data.get(str(user_id), {})

    cities = user_info.get("cities", { })
    cities.pop(name, None)

    save_json(data)


def get_user_activities(my_id):
    try:
        user_info = load_json().get(str(my_id))
        activities = user_info["active_activities"]
        return activities
    except:
        return []
