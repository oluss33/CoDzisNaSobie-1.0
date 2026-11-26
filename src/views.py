import flet as ft
import api
import database_manager
import json_manager
from city_info import CityCard, WeatherDetails
from city import City

class AuthView(ft.Column):
    def __init__(self, page, connection, on_login_success = None):
        super().__init__()
        self.my_page = page
        self.connection = connection
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.alignment = ft.MainAxisAlignment.START
        self.spacing = 12
        self.on_login_success = on_login_success

        self.header_text = ft.Text("Zarejestruj się", size=26, weight=ft.FontWeight.BOLD)
        self.navbar_test = ft.Tabs(selected_index = 0, on_change = self.on_navbar_change,
            length=2,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
                controls=[
                    ft.TabBar(
                        tab_alignment=ft.TabAlignment.CENTER,
                        tabs=[
                            ft.Tab(label=ft.Text("Register")),
                            ft.Tab(label=ft.Text("Login"))
                        ]
                    )
                ]
            )
        )
        self.icon = ft.Icon(ft.Icons.LOCK_PERSON_OUTLINED, size=80, color=ft.Colors.WHITE)
        self.usernameField = ft.CupertinoTextField(placeholder_text="Nazwa użytkownika")
        self.passwordField = ft.CupertinoTextField(placeholder_text="Hasło", password=True)
        self.btn = ft.Button(content="Zarejestruj się", on_click=self.auth_user_click)
        self.controls = [self.navbar_test, self.header_text, self.icon,self.usernameField, self.passwordField, self.btn]

    def handle_auth(self):
        if self.navbar_test.selected_index == 0:
            self.btn.content = "Zarejestruj się"
            self.header_text.value = "Zarejestruj się"
            self.icon.icon = ft.Icons.LOCK_PERSON_OUTLINED
        else:
            self.btn.content = "Zaloguj się"
            self.header_text.value = "Zaloguj się"
            self.icon.icon = ft.Icons.PERSON_OUTLINE

        self.my_page.update()

    def on_navbar_change(self, e):
        selected_index = e.control.selected_index

        self.handle_auth()

    def auth_user_click(self, e):
        username = self.usernameField.value.strip()
        password = self.passwordField.value.strip()
        if not username or not password:
            self.my_page.show_dialog(ft.SnackBar(content=ft.Text("Wypełnij wszystkie pola", color=ft.Colors.WHITE),
                                                 bgcolor=ft.Colors.RED_700))
            return
        if self.navbar_test.selected_index == 0:
            try:
                if database_manager.add_user(self.connection, username, password):
                    self.my_page.show_dialog(ft.SnackBar(
                        content=ft.Text("Zarejestrwano pomyslnie. Mozesz sie od teraz zalogowac.", color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.GREEN_700
                    ))
                    self.usernameField.value = ""
                    self.passwordField.value = ""
                    self.my_page.update()
                else:
                    self.my_page.show_dialog(ft.SnackBar(content=ft.Text("Istnieje juz taka nazwa uzytkownika w bazie danych. Sprobuj ponownie.", color=ft.Colors.WHITE), bgcolor=ft.Colors.AMBER_800))
            except Exception as e:
                print("cos nie tak", e)
        else:
            if database_manager.login_user(self.connection, username, password):
                self.my_page.show_dialog(ft.SnackBar(
                    content=ft.Text("Zalogowano pomyslnie.", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.GREEN_700
                ))
                self.my_page.session.store.set("username", username)
                self.my_page.session.store.set("id", database_manager.get_user_id(self.connection, username))

                if self.on_login_success:
                    self.on_login_success()
                self.usernameField.value = ""
                self.passwordField.value = ""
                self.my_page.update()

            else:
                self.my_page.show_dialog(ft.SnackBar(content=ft.Text("Bledne haslo lub nazwa uzytkownika!", color=ft.Colors.WHITE, ), bgcolor=ft.Colors.RED_400))
class AccountView(ft.Column):
    def __init__(self, page, on_logout_success = None):
        super().__init__()
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.my_page = page
        self.on_logout_sucess = on_logout_success
        self.width = 600
        username = self.my_page.session.store.get("username")
        self.header_test = ft.Text(f"Witaj, {username}")

        self.logout_btn = ft.Button(content = ft.Text("Log out", color=ft.Colors.WHITE), bgcolor=ft.Colors.RED_400, on_click=self.logout)

        self.saved_activities = json_manager.get_user_activities(self.my_page.session.store.get("id"))
        # self.activities = ["Bieganie", "Wrażliwość na zimno", "Odporność na zimno", "Częste spacery", "Trening siłowy", "Rzadkie wyjścia z domu", "Wrażliwość na wysokie ciśnienie", "Jazda na rowerze", "Wrażliwość na wiatr", "Częste przeziębienia"]
        self.activities_dict = {
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
        self.activity_buttons = []

        for activity in self.activities_dict.keys():
            activity_btn = ft.Button(content=activity, color=ft.Colors.BLACK if self.activities_dict[activity] in self.saved_activities else ft.Colors.WHITE, width=200, bgcolor=None if not self.activities_dict[activity] in self.saved_activities else ft.Colors.GREEN_700, on_click=self.toggle_activity(activity))
            self.activity_buttons.append(activity_btn)

        #self.is_running = "running" in saved
        #self.is_cold = "cold" in saved

        # self.btn_running = ft.Button(content="Bieganie", color=ft.Colors.BLACK if self.is_running else ft.Colors.WHITE,width=200,bgcolor=None if not self.is_running else ft.Colors.GREEN_700, on_click=self.toggle_running)
        # self.btn_cold = ft.Button(content="Wrazliwosc na zimno", color=ft.Colors.BLACK if self.is_cold else ft.Colors.WHITE, width=200, bgcolor=None if not self.is_cold else ft.Colors.GREEN_700, on_click=self.toggle_cold)
        self.controls = [self.header_test, *self.activity_buttons, self.logout_btn]

    def toggle_activity(self, activity):
        def on_click_handler(e):
            is_active = self.activities_dict[activity] in self.saved_activities

            if not is_active:
                self.saved_activities.append(self.activities_dict[activity])
                e.control.color = ft.Colors.BLACK
                e.control.bgcolor = ft.Colors.GREEN_700
            else:
                self.saved_activities.remove(self.activities_dict[activity])
                e.control.color = ft.Colors.WHITE
                e.control.bgcolor = None
            self.save_activities()
        return on_click_handler

    def save_activities(self):
        json_manager.save_user_activities(self.my_page.session.store.get("id"), self.saved_activities)

    def logout(self):
        self.my_page.session.store.set("username", None)
        self.my_page.session.store.set("id", None)
        self.my_page.update()

        if self.on_logout_sucess:
            self.on_logout_sucess()

    '''    def toggle_running(self):
            self.is_running = not self.is_running
            self.btn_running.bgcolor = None if not self.is_running else ft.Colors.GREEN_700
            self.btn_running.color = ft.Colors.BLACK if self.is_running else ft.Colors.WHITE
            self.btn_running.update()
            self.save_activities()

        def toggle_cold(self):
            self.is_cold = not self.is_cold
            self.btn_cold.bgcolor = None if not self.is_cold else ft.Colors.GREEN_700
            self.btn_cold.color = ft.Colors.BLACK if self.is_cold else ft.Colors.WHITE
            self.btn_cold.update()
            self.save_activities()'''

class SearchView(ft.Column):
    def __init__(self, page):
        super().__init__()
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.my_page = page

        self.search_field = ft.CupertinoTextField(placeholder_text="Wpisz nazwę miasta", width=300)

        self.columns = ft.Column(spacing=8, width=400, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.weather_container = ft.Column(spacing=8, width=800, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        self.search_button = ft.Button(content="Szukaj", on_click=self.find_weather)
        self.search_field.on_submit = self.find_weather
        self.favorites_btn = None
        self.controls = [self.search_field, self.columns, self.weather_container, self.search_button]

    def find_weather(self, e):
        self.columns.controls.clear()
        self.weather_container.controls.clear()
        founds = api.find_city(self.search_field.value, self.my_page)
        if not founds:
            self.my_page.show_dialog(
                ft.SnackBar(
                    content = ft.Text("Nie znaleziono miasta")
                )
            )
            return

        for city in founds:
            city_card = CityCard(city, self.choose_city(city))

            self.columns.controls.append(city_card)
        self.my_page.update()



    def choose_city(self, city):
        def on_click_handler(e):
            self.weather_container.controls.clear()
            self.columns.controls.clear()

            weather_details = WeatherDetails(city, self.my_page, on_back=self.on_back)
            self.weather_container.controls.append(weather_details)
            self.my_page.update()
        return on_click_handler

    def on_back(self):
        self.weather_container.controls.clear()
        self.my_page.update()

class FavoritesView(ft.Column):
    def __init__(self, page):
        super().__init__()
        self.my_page = page
        self.alignment = ft.MainAxisAlignment.CENTER
        self.text_test = ft.Text("Ulubione miasta", size=24, weight=ft.FontWeight.BOLD)
        self.search_container = ft.Column(width=1000, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.controls = [self.search_container]
        fav_cities = self.generate_fav_cities()
        self.draw_fav_cities(fav_cities)


    def generate_fav_cities(self):
        cities = json_manager.get_fav_cities(self.my_page.session.store.get("id"))

        print(cities)

        fav_cities = []

        for key, value in cities.items():
            name = key.split(";")[0]
            lon = value[0]
            lat = value[1]
            country = value[2]
            admin = value[3]

            city = City(self.my_page, name,  country, admin, lat, lon)
            fav_cities.append(city)

        return fav_cities
    def draw_fav_cities(self, fav_cities : list):
        self.search_container.controls.clear()
        for city in fav_cities:
            city_card = CityCard(city, on_click=self.choose_city(city))

            self.search_container.controls.append(city_card)

        self.my_page.update()

    def choose_city(self, city):
        def on_click_handler(e):
            self.search_container.controls.clear()
            weather_details = WeatherDetails(city, self.my_page, on_back=self.on_back)
            self.search_container.controls.append(weather_details)
            self.my_page.update()
        return on_click_handler

    def on_back(self):
        self.search_container.controls.clear()
        self.my_page.update()
