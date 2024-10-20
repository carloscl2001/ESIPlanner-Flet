import flet as ft
from home_view import Home
from agenda_view import Agenda
from timetable_view import Timetable
from profile_view import Profile

def main(page: ft.Page):
    # Define las vistas
    views = {
        0: Home().content,
        1: Agenda().content,
        2: Timetable().content,
        3: Profile().content,
    }

    # Función para cambiar la vista
    def change_view(selected_index):
        page.clean()

        # Añadir el NavigationBar y establecer la vista seleccionada
        page.add(ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.icons.HOME_ROUNDED, label="Home"),
                ft.NavigationBarDestination(icon=ft.icons.CALENDAR_MONTH_OUTLINED, label="Agenda"),
                ft.NavigationBarDestination(icon=ft.icons.CALENDAR_VIEW_WEEK, label="Horario"),
                ft.NavigationBarDestination(icon=ft.icons.PERSON_ROUNDED, label="Perfil"),
            ],
            selected_index=selected_index,  # Establece el índice seleccionado
            on_change=lambda e: change_view(e.control.selected_index),
        ))

        # Añadir la vista seleccionada usando el índice
        page.add(views[selected_index])

    # Cambia a la vista de inicio
    change_view(0)  

ft.app(target=main)
