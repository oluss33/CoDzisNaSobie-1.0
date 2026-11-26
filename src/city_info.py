import flet as ft
import api
import custom_charts
import json_manager
import ai_api

import datetime

class CityCard(ft.Container):
    def __init__(self, city, on_click = None):
        super().__init__()
        self.city = city
        self.width = 350
        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text(f"{city.name} ( {city.admin} )", weight=ft.FontWeight.BOLD, size=15),
                ft.Text(f"{city.country}", color=ft.Colors.GREY_400, size=12)],
        )
        self.padding = 12
        self.border_radius = 8
        self.bgcolor = ft.Colors.SURFACE_CONTAINER_HIGHEST
        self.ink = True
        self.on_click = on_click


class WeatherDetails(ft.Column):
    def __init__(self, city, page, on_back=None):
        super().__init__()
        weather = api.get_weather(city.name, city.lat, city.lon)
        self.city = city
        self.my_page = page
        self.temperature = weather.temperature
        self.wind = weather.wind
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.rain = weather.rain
        self.snowfall = weather.snowfall
        self.probability = weather.precipitation_probability
        self.current_hour = weather.current_hour
        hourly_pressure = weather.hourly_pressure
        pressure = weather.pressure
        '''text_color = ft.Colors.WHITE
        if pressure > 1020:
            text_color = ft.Colors.RED_400
        if pressure < 1000:
            text_color = ft.Colors.YELLOW_400'''
        hourly_temp = weather.hourly_temp
        self.weather_code = weather.weather_code
        self.my_chart = custom_charts.create_chart(hourly_temp)
        self.max_width = 1200
        self.padding = 16
        self.border_radius = 10
        self.favorites_btn = ft.Button(icon=ft.Icons.STAR,
                                       color=ft.Colors.YELLOW_400 if city.is_favorite else ft.Colors.GREY_400,
                                       on_click=self.favorite_city_handler(city))
        self.back_btn = ft.Button(icon=ft.Icons.ARROW_BACK_IOS_NEW_OUTLINED, on_click=on_back)

        print("activities:", json_manager.get_user_activities(self.my_page.session.store.get("id")))
        tips = ai_api.generate_suggestions(weather, json_manager.get_user_activities(self.my_page.session.store.get("id")))

        self.navbar = ft.SegmentedButton(on_change=self.handle_selection_change, selected=["1"], segments=[ ft.Segment(value="1", label=ft.Text("Pogoda"), icon=ft.Icons.CLOUD),
                ft.Segment(value="2", label=ft.Text("Opady"), icon=ft.Icons.CLOUDY_SNOWING)])
        self.weather_tab = self.generate_weather_content(pressure, tips)
        self.precipitation_tab = self.generate_precipitation(weather.precipitation)
        self.controls = [self.navbar, self.weather_tab, ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[self.favorites_btn, self.back_btn])]


    def generate_weather_content(self, pressure, tips):

        current_hour = self.current_hour

        local_content = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=800, alignment=ft.MainAxisAlignment.CENTER,controls=[
            ft.Text(f"{self.city.name}", weight=ft.FontWeight.BOLD, size=23),
            ft.Text(size=18,
                    spans=[
                        ft.TextSpan("Temperatura: ", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                        ft.TextSpan(f"{self.temperature}°C"),
                    ]),
            ft.Text(size=18, spans=[
                ft.TextSpan(f"Wiatr: ", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                ft.TextSpan(f"{self.wind} km/h")]),
            ft.Text(size=18, spans=[
                ft.TextSpan(f"Kod pogody: ", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                ft.TextSpan(f"{api.translate_weather_code(self.weather_code)}")
            ]),
            ft.Text(size=18, spans=[
                ft.TextSpan("Ciśnienie: ", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                ft.TextSpan(f"{pressure} hPa")
            ]),
            ft.Text(size=18,spans=[
                ft.TextSpan("Szansa opadów (od teraz): ", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                ft.TextSpan(f"{max(self.probability[current_hour:])} %")
            ]),
            ft.Text(size=18, spans=[
                ft.TextSpan("Opady deszczu: ", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                ft.TextSpan(f"{round(sum(self.rain), 1)} mm")
            ]),
            ft.Text(size=18, spans=[
                ft.TextSpan("Opady śniegu: ", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                ft.TextSpan(f"{round(sum(self.snowfall), 1)} cm")
            ]),
            self.my_chart, ft.Text(tips, size=18),
                   ])

        return local_content

    def generate_precipitation(self, precipitation):
        chart = custom_charts.create_bar_chart(precipitation)
        local_content = ft.Column(width=1200, alignment=ft.MainAxisAlignment.CENTER,controls=[chart])
        return local_content

    def handle_selection_change(self, e):
        if "1" in e.control.selected:
            self.controls[1] = self.weather_tab
        if "2" in e.control.selected:
            self.controls[1] = self.precipitation_tab
        self.update() # update SAMEJ kolumny, bez calej strony
    def favorite_city_handler(self, city):
        name = city.name
        lat = city.lat
        lon = city.lon
        def on_click_handler(e):

            user_id = self.my_page.session.store.get("id")
            if user_id is None:
                self.my_page.show_dialog(ft.SnackBar(content=ft.Text("Zaloguj się aby zapisać ulubione miasto")))
                return

            if not city.is_favorite:
                json_manager.add_city(self.my_page.session.store.get("id"), city.name, city.lat, city.lon, city.country, city.admin)
            else:
                json_manager.remove_city(self.my_page.session.store.get("id"), name, lat, lon)

            city.is_favorite = not city.is_favorite
            self.favorites_btn.color = ft.Colors.YELLOW_400 if city.is_favorite else ft.Colors.GREY_400
            self.favorites_btn.update()
        return on_click_handler
