import flet as ft
from home_view import Home
from agenda_view import Agenda
from timetable_view import Timetable
from profile_view import Profile
from login_view import Login
from register_view import Register

# Variables globales para almacenar autenticación y nombre de usuario
authenticated = False
username = ""  # Aquí se almacenará el nombre de usuario

def main(page: ft.Page):
    global authenticated, username  # Añadir 'username' como global

    # Función para cambiar la vista
    def change_view(selected_index):
        # Limpiar el contenido actual de la página
        page.clean()

        # Añadir el NavigationBar y establecer la vista seleccionada si el usuario está autenticado
        if authenticated:
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

            # Define las vistas como instancias de las clases
            views = {
                0: Home(),
                1: Agenda(),
                2: Timetable(),
                3: Profile(username),  # Pasar el nombre de usuario a la vista de perfil
            }

            # Añadir la vista seleccionada usando su atributo `content`
            page.add(views[selected_index].content)

    # Función para manejar el login o registro exitoso
    def on_login_success(user):
        global authenticated, username
        authenticated = True
        username = user  # Guardar el nombre de usuario
        change_view(3)  # Cambia a la vista de perfil

    # Mostrar la pantalla de registro o login si el usuario no está autenticado
    if not authenticated:
        page.clean()
        # Puedes elegir cuál mostrar: login o register
        # page.add(Login(on_success=on_login_success))  # Descomenta para login
        page.add(Register(on_success=on_login_success))  # Descomenta para registro

    else:
        change_view(0)  # Cambia a la vista de inicio si el usuario ya está autenticado

# Ejecutar la app
ft.app(target=main)
