import flet as ft
from views.home_view import home_view
from views.store_view import store_view
from views.product_view import product_view

def main(page: ft.Page):
    page.title = "Routes Example"
    page.theme_mode = "light"

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(home_view(page))
        elif page.route == "/store":
            page.views.append(store_view(page))
        elif page.route == "/store/product":
            page.views.append(product_view(page))
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(main)