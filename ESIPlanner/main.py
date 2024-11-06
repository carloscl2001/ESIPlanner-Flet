import flet as ft
import requests  # Necesario para hacer la petición HTTP

from home_view import Home
from agenda_view import Agenda
from timetable_view import Timetable
from profile_view import Profile

# Variables globales para autenticación y nombre de usuario
authenticated = False
username = ""

# Funciones principales
def main(page: ft.Page):
    global authenticated, username

    # Mostrar la vista principal (página de inicio)
    def show_main_view():
        change_view(0)  # Cambia a la vista de inicio

    # Cambiar entre vistas
    def change_view(selected_index):
        page.clean()  # Limpiar el contenido actual de la página

        # Añadir el NavigationBar
        page.add(ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.icons.HOME_ROUNDED, label="Home"),
                ft.NavigationBarDestination(icon=ft.icons.CALENDAR_MONTH_OUTLINED, label="Agenda"),
                ft.NavigationBarDestination(icon=ft.icons.CALENDAR_VIEW_WEEK, label="Horario"),
                ft.NavigationBarDestination(icon=ft.icons.PERSON_ROUNDED, label="Perfil"),
            ],
            selected_index=selected_index,
            on_change=lambda e: change_view(e.control.selected_index),
        ))

        # Define las vistas
        views = {
            0: Home(),
            1: Agenda(),
            2: Timetable(),
            3: Profile(username, on_logout=logout),  # Pasa la función de logout
        }

        page.add(views[selected_index].content)

    # Lógica de autenticación
    def login_clicked(e):
        user = username_input.value
        password = password_input.value

        try:
            response = requests.post(
                "http://127.0.0.1:8000/auth/login",
                data={"username": user, "password": password}
            )
            if response.status_code == 200:
                data = response.json()
                token = data.get("access_token")
                if token:
                    global authenticated, username
                    authenticated = True
                    username = user
                    show_main_view()  # Muestra la vista principal tras autenticarse
                else:
                    error_text.value = "Error: Token no recibido."
            else:
                error_text.value = "Error de inicio de sesión. Verifique sus credenciales."
        except requests.RequestException as ex:
            error_text.value = f"Error de conexión: {ex}"

        page.update()  # Actualizar la página para reflejar el mensaje de error

    # Lógica de registro
    def register_clicked(e):
        new_user_data = {
            "email": email_input.value,
            "username": reg_username_input.value,
            "password": reg_password_input.value,
            "name": name_input.value,
            "surname": surname_input.value,
            "degree": degree_input.value
        }

        try:
            response = requests.post("http://127.0.0.1:8000/users/", json=new_user_data)
            if response.status_code == 201:
                global authenticated, username
                authenticated = True
                username = new_user_data["username"]
                show_main_view()  # Muestra la vista principal tras registro exitoso
            else:
                register_error_text.value = "Error de registro. Verifique los datos ingresados."
        except requests.RequestException as ex:
            register_error_text.value = f"Error de conexión: {ex}"

        page.update()  # Actualizar la página para reflejar el mensaje de error

    # Pantalla de registro
    def show_register_form(e=None):  # Añadir el parámetro e
        page.clean()

        global reg_username_input, reg_password_input, email_input, name_input, surname_input, degree_input, register_error_text

        email_input = ft.TextField(label="Correo electrónico", width=200)
        reg_username_input = ft.TextField(label="Usuario", width=200)
        reg_password_input = ft.TextField(label="Contraseña", password=True, width=200)
        name_input = ft.TextField(label="Nombre", width=200)
        surname_input = ft.TextField(label="Apellido", width=200)
        degree_input = ft.TextField(label="Grado", width=200)
        register_button = ft.ElevatedButton("Registrarse", on_click=register_clicked)
        register_error_text = ft.Text(color="red")

        page.add(
            ft.Column(
                [
                    ft.Text("Registro de Usuario", size=30),
                    email_input,
                    reg_username_input,
                    reg_password_input,
                    name_input,
                    surname_input,
                    degree_input,
                    register_button,
                    register_error_text,
                    ft.TextButton("¿Ya tienes una cuenta? Inicia sesión", on_click=show_login_form),
                    ft.TextButton("Volver al inicio de sesión", on_click=show_login_form),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        page.update()

    # Pantalla de inicio de sesión
    def show_login_form(e=None):  # Añadir el parámetro e
        page.clean()

        global username_input, password_input, error_text
        username_input = ft.TextField(label="Usuario", width=200)
        password_input = ft.TextField(label="Contraseña", password=True, width=200)
        login_button = ft.ElevatedButton("Iniciar sesión", on_click=login_clicked)
        error_text = ft.Text(color="red")

        page.add(
            ft.Column(
                [
                    ft.Text("Iniciar sesión", size=30),
                    username_input,
                    password_input,
                    login_button,
                    error_text,
                    ft.TextButton("¿No tienes cuenta? Regístrate", on_click=show_register_form),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        page.update()

    # Función para cerrar sesión
    def logout(e):
        global authenticated, username
        authenticated = False
        username = ""
        show_login_form()  # Redirige al formulario de inicio de sesión

    # Si no está autenticado, mostrar el formulario de inicio de sesión
    if not authenticated:
        show_login_form()
    else:
        show_main_view()


# Ejecutar la app
ft.app(target=main)
