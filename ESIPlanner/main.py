# main.py
import flet as ft
from navigation_bar import NavigationBarComponent  # Importar la clase
import requests

def main(page: ft.Page):

    page.title = "NavigationBar Example"

    # Crear una instancia de NavigationBarComponent
    nav_bar_component = NavigationBarComponent()

    # Cambiar el color de fondo de la página
    page.bgcolor = ft.colors.WHITE

    # Asignar el NavigationBar creado por la clase
    page.navigation_bar = nav_bar_component.get_navigation_bar()

    # Hacer una solicitud al backend FastAPI
    response = requests.get("http://127.0.0.1:8000")
    data = response.json()

    # Mostrar los eventos en la interfaz de Flet
    page.add(ft.Text("El servidor nos dice:"))

    page.add(ft.Text(data["message"]))

ft.app(main)