import flet as ft

def product_view(page):
    return ft.View(
        "/store/product",
        [
            ft.AppBar(title=ft.Text("Product"), bgcolor=ft.colors.SURFACE_VARIANT),
            ft.ElevatedButton("Go Store", on_click=lambda _: page.go("/store")),
        ],
    )
