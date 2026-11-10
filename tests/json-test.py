import json

def odczyt():
    my_data = { }
    with open("test.json", "r") as my_file:
        my_data = json.load(my_file)

    return my_data
def zapis():
    username = input("username: ")
    id = int(input("id: "))

    count = int(input("how many fav cities: "))

    fav_cities = []

    for i in range(count):
        fav_city = input("fav city: ")
        fav_cities.append(fav_city)

    _data = { "username": username,
             "id": id,
             "fav_cities": fav_cities
             }

    with open("test.json", "w") as my_file:
        json.dump(_data, my_file)

choice = int(input("zapis(1) czy odczyt (2): "))

if choice == 1:
    zapis()

if choice == 2:
    gowno = odczyt()
    print(gowno)