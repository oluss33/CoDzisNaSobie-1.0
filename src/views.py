import flet as ft
import api
import custom_charts

class LoginView(ft.Column):
    def __init__(self, page):
        super().__init__()
        self.my_page = page
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.text = ft.Text("Siema kurwa")

        self.controls = [self.text]

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


            self.weather_container.controls.append(info_card)
            self.my_page.update()
        return on_click_handler