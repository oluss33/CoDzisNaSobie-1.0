import json
import os

FILE_PATH = "data/data.json"

def load_json():

    if not os.path.exists(FILE_PATH):
        return { }
    try:
        with open(FILE_PATH, "r") as my_file:
            return json.load(my_file)
    except:
        return { }

def save_json(data):
    with open(FILE_PATH, "w") as my_file:
        json.dump(data, my_file)

def save_user_activities(user_id, active_activities : list):
    print("zapisuje uesr activitiy")
    data = load_json()

    if user_id not in data.keys():
        data[str(user_id)] = {}

    data[str(user_id)]["active_activities"] = active_activities

    save_json(data)


def get_user_activities(my_id):
    try:
        user_info = load_json().get(str(my_id))
        activities = user_info["active_activities"]
        return activities
    except:
        return []
