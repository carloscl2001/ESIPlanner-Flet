import flet as ft
from home import Home
from agenda import Agenda
from horario import Horario
from perfil import Perfil

def main(page: ft.Page):
    # Define las vistas
    views = {
        0: Home(),
        1: Agenda(),
        2: Horario(),
        3: Perfil(),
    }

    # Función para cambiar la vista
    def change_view(selected_index):
        page.clean()

        # Añadir el NavigationBar y establecer la vista seleccionada
        page.add(ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.icons.HOME, label="Home"),
                ft.NavigationBarDestination(icon=ft.icons.LIST, label="Agenda"),
                ft.NavigationBarDestination(icon=ft.icons.SCHEDULE, label="Horario"),
                ft.NavigationBarDestination(icon=ft.icons.PERSON, label="Perfil"),
            ],
            selected_index=selected_index,  # Establece el índice seleccionado
            on_change=lambda e: change_view(e.control.selected_index),
        ))

        # Añadir la vista seleccionada usando el índice
        page.add(views[selected_index])

    # Inicializar la vista
    page.window.width = 800
    page.window.height = 600
    change_view(0)  # Cambia a la vista de inicio

ft.app(target=main)
