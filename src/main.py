import flet as ft
from flet import MainAxisAlignment, CrossAxisAlignment
import api
import custom_charts

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
            weather = api.get_weather(name, lat, lon)

            temperature = weather.temperature
            wind = weather.wind
            temp_hourly = weather.temp_hourly

            my_chart = custom_charts.create_chart(temp_hourly)
            info_card = ft.Container(width=600, padding=16, border_radius=10, content=ft.Row(width=600, alignment=MainAxisAlignment.CENTER, controls=[ft.Container(content=ft.Column(alignment=MainAxisAlignment.CENTER,controls=[
                        ft.Text(f"{name}", weight=ft.FontWeight.BOLD, size=23),
                        ft.Text(f"Temperatura: {temperature}°C", size=16),
                        ft.Text(f"Wiatr: {wind} km / h", size=16),
                        my_chart]))]))


            weather_container.controls.append(info_card)
            page.update()
        return on_click_handler


    def find_weather(e):
        columns.controls.clear()
        weather_container.controls.clear()
        founds = api.find_city(search_field.value)
        if not founds:
            page.show_dialog(
                ft.SnackBar(
                    content = ft.Text("Nie znaleziono miasta")
                )
            )
            return

        for city in founds:


            city_card = ft.Container(width=350,
                content=ft.Column(alignment=MainAxisAlignment.CENTER,controls=[
                        ft.Text(f"{city.name} ( {city.admin} )",weight=ft.FontWeight.BOLD, size=15),
                        ft.Text(f"{city.country}", color=ft.Colors.GREY_400, size=12)]),
                padding=12,
                border_radius = 8,
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                ink=True,
                on_click=choose_city(city.name, city.lat, city.lon)
            )

            columns.controls.append(city_card)
        page.update()


    search_button = ft.Button(content="Szukaj", on_click=find_weather)
    search_field.on_submit = find_weather

    header = ft.Row(alignment=MainAxisAlignment.CENTER,
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

    page.add(header, layout, columns, weather_container)

if __name__ == "__main__":
    ft.run(main)
