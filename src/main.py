import flet as ft
from flet import MainAxisAlignment, CrossAxisAlignment
import urllib.parse
import urllib.request
import json
import flet_charts as fch

def main(page: ft.Page):

    page.title = "Co dzis na sobie? :)"
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    header_text = ft.Text("Co dzis na sobie?", size=23, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)

    search_field = ft.CupertinoTextField(placeholder_text="Wpisz nazwę miasta", width=300)

    columns = ft.Column(spacing=8, width=400, horizontal_alignment=CrossAxisAlignment.CENTER)
    weather_container = ft.Column(spacing=8, width=800, horizontal_alignment=CrossAxisAlignment.CENTER)


    def choose_city(name, lat, lon):
        def on_click_handler(e):
            weather_container.controls.clear()
            columns.controls.clear()
            weather = get_weather(name, lat, lon)

            temperature = weather[0]
            wind = weather[1]
            temp_hourly = weather[2]

            my_chart = create_chart(temp_hourly)
            info_card = ft.Container(width=600, padding=16, border_radius=10, content=ft.Row(width=600, alignment=MainAxisAlignment.CENTER, controls=[ft.Container(content=ft.Column(alignment=MainAxisAlignment.CENTER,controls=[
                        ft.Text(f"{name}", weight=ft.FontWeight.BOLD, size=23),
                        ft.Text(f"Temperatura: {temperature}°C", size=16),
                        ft.Text(f"Wiatr: {wind} km / h", size=16),
                        my_chart]))]))


            weather_container.controls.append(info_card)
            page.update()
        return on_click_handler

    def create_chart(hourly_temps):
        points = []
        for i in range(len(hourly_temps)):
            hour = f"{i:02d}:00"
            temp = f"{hourly_temps[i]}°C"


            points.append(fch.LineChartDataPoint(x=i, y=hourly_temps[i], tooltip=fch.LineChartDataPointTooltip(text=f"{hour} : {temp}",
                text_style=ft.TextStyle(
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE
                )
            )))

        line = fch.LineChartData(color = ft.Colors.BLUE_GREY_300,
                                curved = False,
                                points = points)

        axis_labels = []
        for h in range(0, 24, 3):
            label_text=f"{h:02d}:00"
            axis_labels.append(
                fch.ChartAxisLabel(
                    value=h,
                    label=ft.Text(label_text, size=10, color=ft.Colors.GREY_400)
                )
            )

        bottom_axis = fch.ChartAxis(
            labels=axis_labels,
        )

        chart = fch.LineChart(data_series=[line], width=500, height=150, bottom_axis=bottom_axis, tooltip=fch.LineChartTooltip(
            bgcolor = ft.Colors.TRANSPARENT,

        ) )

        return chart

    def szukaj_pogody(e):
        columns.controls.clear()
        weather_container.controls.clear()
        founds = szukaj(search_field.value)
        if not founds:
            print("err")
            return

        for city in founds:
            name = city[0]
            country = city[1]
            admin = city[2]
            lat = city[3]
            lon = city[4]


            city_card = ft.Container(width=350,
                content=ft.Column(alignment=MainAxisAlignment.CENTER,controls=[
                        ft.Text(f"{name} ( {admin} )",weight=ft.FontWeight.BOLD, size=15),
                        ft.Text(f"{country}", color=ft.Colors.GREY_400, size=12)]),
                padding=12,
                border_radius = 8,
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                ink=True,
                on_click=choose_city(name, lat, lon)
            )

            columns.controls.append(city_card)
        page.update()


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
        my_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m&forecast_days=1"
        header = {"User-Agent": "CoDzisNaSobie/1.0"}
        req = urllib.request.Request(my_url, headers=header)

        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))

        temperature = data["current"]["temperature_2m"]
        wind = data["current"]["wind_speed_10m"]

        hourly_temp = data["hourly"]["temperature_2m"]

        print(f"POGODA DLA {name.upper()}")
        print(f"tempeartura: {temperature}")
        print(f"wiatr: {wind} km/h")

        return temperature, wind, hourly_temp

    search_button = ft.Button(content="Szukaj", on_click=szukaj_pogody)
    search_field.on_submit = szukaj_pogody

    test = ft.Row(alignment=MainAxisAlignment.CENTER,
                  spacing=10,
                  controls=[
                      header_text
                  ])

    layout = ft.Row(
        alignment=MainAxisAlignment.CENTER,
        spacing=20,
        controls=[
            search_field, search_button
        ]
    )

    page.add(test, layout, columns, weather_container)

if __name__ == "__main__":
    ft.run(main)
