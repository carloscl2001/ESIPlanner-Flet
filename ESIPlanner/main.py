# main.py
import flet as ft
from navigation_bar import NavigationBarComponent  # Importar la clase

def main(page: ft.Page):

    page.title = "NavigationBar Example"

    # Crear una instancia de NavigationBarComponent
    nav_bar_component = NavigationBarComponent()

    # Cambiar el color de fondo de la página
    page.bgcolor = ft.colors.WHITE

    # Asignar el NavigationBar creado por la clase
    page.navigation_bar = nav_bar_component.get_navigation_bar()

    # Agregar contenido adicional a la página
    page.add(ft.SafeArea(ft.Text("Hello, Flet!")))

ft.app(main)