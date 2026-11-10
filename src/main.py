import flet as ft
from flet import MainAxisAlignment, CrossAxisAlignment
import views
import sqlite3
import database_manager
def main(page: ft.Page):

    def on_logout_success():
        body_container.content = login_view_type_shit
        page.update()

    def on_login_success():
        body_container.content = views.AccountView(page, on_logout_success)
        page.update()
    #print("testuje cos, ", page.session.store.get("user"))

    connection = sqlite3.connect("../tests/test-db.db")
    login_view_type_shit = views.AuthView(page, connection, on_login_success)
    search_view = views.SearchView(page)
    body_container = ft.Container(content = search_view, expand = True)

    def on_navbar_change(e):
        selected_index = e.control.selected_index

        if selected_index == 0:
            body_container.content = search_view
        if selected_index == 1:
            user = page.session.store.get("username")
            if not user:
                body_container.content = login_view_type_shit
            else:
                on_login_success()
        if selected_index == 2:
            print("favorites kliknieto")

        page.update()

    navbar = ft.Tabs(selected_index = 0, on_change = on_navbar_change,
        length=3,
        content=ft.Row(
            controls=[
                ft.TabBar(
                    tabs=[ft.Tab(label="Wyszukaj miasto", icon=ft.Icons.SEARCH),
                          ft.Tab(label="Konto", icon=ft.Icons.PERSON),
                          ft.Tab(label="Zapisane", icon=ft.Icons.STAR)]
                )
            ]
        )
    )

    page.title = "Co dzis na sobie? :)"
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    header_text = ft.Text("Co dzis na sobie?", size=23, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)

    header = ft.Row(alignment=MainAxisAlignment.CENTER,
                  spacing=10,
                  controls=[
                      header_text
                  ])

    '''layout = ft.Row(
        alignment=MainAxisAlignment.CENTER,
        spacing=20,
        controls=[
            search_field, search_button
        ]
    )'''

    #page.add(navbar,header, layout, columns, weather_container)
    page.add(navbar, header, body_container)

    def on_exit(e):
        database_manager.close_db(connection)
    page.on_disconnect = on_exit



if __name__ == "__main__":
    ft.run(main)
