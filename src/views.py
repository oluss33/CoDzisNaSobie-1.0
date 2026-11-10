import flet as ft
import api
import custom_charts
import database_manager
import json_manager

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
        self.usernameField = ft.CupertinoTextField(placeholder_text="Username")
        self.passwordField = ft.CupertinoTextField(placeholder_text="Password", password=True)
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
                task = (username, password)
                if database_manager.add_user(self.connection, task):
                    self.my_page.show_dialog(ft.SnackBar(
                        content=ft.Text("Zarejestrowano pomyslnie. Mozesz sie od teraz zalogowac.", color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.GREEN_700
                    ))
                else:
                    self.my_page.show_dialog(ft.SnackBar(content=ft.Text("Istnieje juz taka nazwa uzytkownika w bazie danych. Sprobuj ponownie.", color=ft.Colors.WHITE, bgcolor=ft.Colors.YELLOW_400)))
            except Exception as e:
                print("cos jeblo", e)
        else:
            if database_manager.login_user(self.connection, username, password):
                self.my_page.show_dialog(ft.SnackBar(
                    content=ft.Text("Zalogowano pomyslnie.", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.GREEN_700
                ))
                self.my_page.session.store.set("username", username)
                self.my_page.session.store.set("id", database_manager.get_user_id(self.connection, username, password))


                if self.on_login_success:
                    self.on_login_success()

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

        saved = json_manager.get_user_activities(self.my_page.session.store.get("id"))
        print(saved)
        self.is_running = "running" in saved

        self.btn_running = ft.Button(content="Bieganie", color=ft.Colors.BLACK if self.is_running else ft.Colors.WHITE,width=200,bgcolor=None if not self.is_running else ft.Colors.GREEN_700, on_click=self.toggle_running)

        self.controls = [self.header_test, self.btn_running, self.logout_btn]

    def toggle_running(self):
        self.is_running = not self.is_running
        self.btn_running.bgcolor = None if not self.is_running else ft.Colors.GREEN_700
        self.btn_running.color = ft.Colors.BLACK if self.is_running else ft.Colors.WHITE
        self.btn_running.update()
        self.save_activities()

    def save_activities(self):
        active_activities = []

        if self.is_running:
            active_activities.append("running")

        json_manager.save_user_activities(self.my_page.session.store.get("id"), active_activities)

    def logout(self):
        self.my_page.session.store.set("username", None)
        self.my_page.session.store.set("id", None)
        self.my_page.update()

        if self.on_logout_sucess:
            self.on_logout_sucess()
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

        self.controls = [self.search_field, self.columns, self.weather_container, self.search_button]

    def find_weather(self, e):
        self.columns.controls.clear()
        self.weather_container.controls.clear()
        founds = api.find_city(self.search_field.value)
        if not founds:
            self.my_page.show_dialog(
                ft.SnackBar(
                    content = ft.Text("Nie znaleziono miasta")
                )
            )
            return

        for city in founds:


            city_card = ft.Container(width=350,
                content=ft.Column(alignment=ft.MainAxisAlignment.CENTER,controls=[
                        ft.Text(f"{city.name} ( {city.admin} )",weight=ft.FontWeight.BOLD, size=15),
                        ft.Text(f"{city.country}", color=ft.Colors.GREY_400, size=12)]),
                padding=12,
                border_radius = 8,
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                ink=True,
                on_click=self.choose_city(city.name, city.lat, city.lon)
            )

            self.columns.controls.append(city_card)
        self.my_page.update()

    def choose_city(self, name, lat, lon):
        def on_click_handler(e):
            self.weather_container.controls.clear()
            self.columns.controls.clear()
            weather = api.get_weather(name, lat, lon)

            temperature = weather.temperature
            wind = weather.wind
            hourly_temp = weather.hourly_temp

            my_chart = custom_charts.create_chart(hourly_temp)
            info_card = ft.Container(width=600, padding=16, border_radius=10, content=ft.Row(width=600, alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Container(content=ft.Column(alignment=ft.MainAxisAlignment.CENTER,controls=[
                        ft.Text(f"{name}", weight=ft.FontWeight.BOLD, size=23),
                        ft.Text(f"Temperatura: {temperature}°C", size=16),
                        ft.Text(f"Wiatr: {wind} km / h", size=16),
                        my_chart]))]))
            favorites_btn = ft.Button(icon=ft.Icons.STAR)


            self.weather_container.controls.append(info_card)
            self.weather_container.controls.append(favorites_btn)
            self.my_page.update()
        return on_click_handler