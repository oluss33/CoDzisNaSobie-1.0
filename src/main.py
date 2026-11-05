import flet as ft
from flet import MainAxisAlignment, CrossAxisAlignment
import views
def main(page: ft.Page):

    login_view_type_shit = views.LoginView(page)
    search_view = views.SearchView(page)
    body_container = ft.Container(content = search_view, expand = True)
    def on_navbar_change(e):
        selected_index = e.control.selected_index

        if selected_index == 0:
            body_container.content = search_view
        if selected_index == 1:
            body_container.content = login_view_type_shit
        if selected_index == 2:
            print("favorites kliknieto")

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

if __name__ == "__main__":
    ft.run(main)
