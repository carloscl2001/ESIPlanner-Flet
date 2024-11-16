import flet as ft
import requests  # Necesario para hacer la petición HTTP
import re  # Importar el módulo re para trabajar con expresiones regulares

from home_view import Home
from agenda_view import Agenda
from timetable_view import Timetable
from profile_view import Profile


# Variables globales para
authenticated = False
username = ""
adding_subjects = None  # Declarar la variable globalmente


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
            0: Home(username),
            1: Agenda(),
            2: Timetable(username),
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

    def register_clicked(e):
        # Verificar que todos los campos obligatorios estén rellenos
        missing_fields = []
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"  # Expresión regular para validar el formato del correo electrónico

        
        # Validación del correo electrónico
        if not email_input.value:
            missing_fields.append("Correo electrónico")
            email_input.border_color = ft.colors.RED
        elif not re.match(email_pattern, email_input.value):  # Validar el formato del correo
            register_error_text.value = "El correo electrónico no tiene un formato válido."
            email_input.border_color = ft.colors.RED
            email_input.focused = True
            page.update()
            return  # Detener el registro si el correo no es válido
        else:
            email_input.border_color = ft.colors.WHITE
        
        if not reg_username_input.value:
            missing_fields.append("Usuario")
            reg_username_input.border_color = ft.colors.RED
        else:
            reg_username_input.border_color = ft.colors.WHITE
        
        if not reg_password_input.value:
            missing_fields.append("Contraseña")
            reg_password_input.border_color = ft.colors.RED
        else:
            reg_password_input.border_color = ft.colors.WHITE
        
        if not name_input.value:
            missing_fields.append("Nombre")
            name_input.border_color = ft.colors.RED
        else:
            name_input.border_color = ft.colors.WHITE
        
        if not surname_input.value:
            missing_fields.append("Apellido")
            surname_input.border_color = ft.colors.RED
        else:
            surname_input.border_color = ft.colors.WHITE
        
        if not degree_input.value:
            missing_fields.append("Grado")
            degree_input.border_color = ft.colors.RED
        else:
            degree_input.border_color = ft.colors.WHITE

        # Si falta algún campo, mostrar un mensaje de error
        if missing_fields:
            register_error_text.value = "Por favor, rellene todos los campos"
            page.update()
            return  # Detener el registro si falta algún campo
        
        # Verificar el estado de la casilla "¿Quieres añadir asignaturas?"
        if adding_subjects.value:
            subjects_to_send = subjects
        else:
            subjects_to_send = []

        new_user_data = {
            "email": email_input.value,
            "username": reg_username_input.value,
            "password": reg_password_input.value,
            "name": name_input.value,
            "surname": surname_input.value,
            "degree": degree_input.value,
            "subjects": subjects_to_send,
        }

        try:
            response = requests.post("http://127.0.0.1:8000/users/", json=new_user_data)
            if response.status_code == 201:
                global authenticated, username
                authenticated = True
                username = new_user_data["username"]
                show_main_view()  # Muestra la vista principal tras registro exitoso
            else:
                register_error_text.value = "Usuario o correo ya registrado."
        except requests.RequestException as ex:
            register_error_text.value = f"Error de conexión: {ex}"

        page.update()  # Actualizar la página para reflejar el mensaje de error


    # Pantalla de inicio de sesión
    def show_register_form(e=None):  # Añadir el parámetro e
        page.clean()

        global reg_username_input, reg_password_input, email_input, name_input, surname_input, degree_input, register_error_text, subjects, adding_subjects  # Incluir adding_subjects

        email_input = ft.TextField(label="Correo electrónico", width=page.width)
        reg_username_input = ft.TextField(label="Usuario", width=page.width)
        reg_password_input = ft.TextField(label="Contraseña", password=True, width=page.width)
        name_input = ft.TextField(label="Nombre", width=page.width)
        surname_input = ft.TextField(label="Apellido", width=page.width)
        degree_input = ft.TextField(label="Grado", width=page.width)
        register_button = ft.CupertinoFilledButton("Registrarse", on_click=register_clicked)
        register_error_text = ft.Text(color="red")

        subjects = []  # Inicializamos las asignaturas
        adding_subjects = ft.CupertinoSwitch(label="¿Quieres añadir a tu perfil alguna asignatura?", value=False, active_color=ft.colors.WHITE)
        message = ft.Text("")  # Mensaje de éxito o error

        # Controles para agregar asignaturas (inicialmente ocultos)
        subject_code_input = ft.TextField(label="Código de asignatura", width=page.width, color=ft.colors.WHITE, visible=False)
        class_types_input = ft.TextField(label="Tipos de clase (separadas por comas)", width=page.width, color=ft.colors.WHITE, visible=False)
        add_subject_button = ft.ElevatedButton("Agregar asignatura", on_click=lambda e: add_subject(), visible=False)
        remove_subject_button = ft.ElevatedButton("Eliminar última asignatura", on_click=lambda e: remove_subject(), visible=False)

        subject_list = ft.Column(visible=False)  # Lista de asignaturas (inicialmente oculta)

        def toggle_subject_fields(e):
            # Mostrar u ocultar los campos de asignaturas según el checkbox
            subject_code_input.visible = adding_subjects.value
            class_types_input.visible = adding_subjects.value and subject_code_input.value != ""
            add_subject_button.visible = adding_subjects.value and subject_code_input.value != ""
            subject_list.visible = adding_subjects.value
            page.update()

        def add_subject():
            code = subject_code_input.value
            types = class_types_input.value.split(",")  # Suponiendo que los tipos se ingresan separados por comas

            # Validar que haya un código de asignatura de exactamente 8 números
            if not code or len(code) != 8 or not code.isdigit():  # Si el código no tiene 8 caracteres o no es numérico
                message.value = "El código de asignatura debe tener exactamente 8 dígitos."
                message.color = ft.colors.RED  # Establecer el color del mensaje a rojo
                subject_code_input.focused = True
                subject_code_input.border_color = ft.colors.RED
                page.update()
                return

            # Validar que se ingrese al menos un tipo de clase
            if not class_types_input.value or len(types) == 0:  # Si el campo está vacío o no tiene elementos
                message.value = "Debes ingresar al menos un tipo de clase para la asignatura."
                message.color = ft.colors.RED  # Establecer el color del mensaje a rojo
                class_types_input.focused = True
                class_types_input.border_color = ft.colors.RED
                page.update()
                return

            # Verificar que los tipos de clase estén correctamente separados por comas (sin puntos u otros caracteres)
            if not re.match(r'^[a-zA-Z0-9, ]*$', class_types_input.value):  # Comprobar si hay caracteres no permitidos (como puntos)
                message.value = "Los tipos de clase solo pueden contener letras mayúsculas y números, además de ir separados por comas."
                message.color = ft.colors.RED  # Establecer el color del mensaje a rojo
                class_types_input.focused = True
                class_types_input.border_color = ft.colors.RED
                page.update()
                return

            # Verificar que todos los tipos de clase estén en mayúsculas
            for type in types:
                if not type.isupper():  # Verificar si el tipo no está en mayúsculas
                    message.value = "Los tipos de clase deben estar en mayúsculas."
                    message.color = ft.colors.RED  # Establecer el color del mensaje a rojo
                    class_types_input.focused = True
                    class_types_input.border_color = ft.colors.RED
                    page.update()
                    return

            # Verificar si los tipos de clase están bien formateados (sin puntos o caracteres no deseados)
            for type in types:
                if type.strip() == "":  # Verificar si hay elementos vacíos (espacios en blanco) entre las comas
                    message.value = "Los tipos de clase deben estar separados por comas sin espacios vacíos."
                    message.color = ft.colors.RED  # Establecer el color del mensaje a rojo
                    class_types_input.focused = True
                    class_types_input.border_color = ft.colors.RED
                    page.update()
                    return

            # Verificar si la asignatura ya está en la lista por el código
            for subject in subjects:
                if subject["code"] == code:
                    message.value = "Ya existe una asignatura con este código."
                    message.color = ft.colors.RED  # Establecer el color del mensaje a rojo
                    subject_code_input.focused = True
                    subject_code_input.border_color = ft.colors.RED
                    page.update()
                    return

            # Validación exitosa, añadir la asignatura
            subjects.append({"code": code, "types": [type.strip() for type in types]})
            subject_code_input.value = ""
            class_types_input.value = ""
            subject_list.controls.append(ft.Text(f"Código: {code}, Tipos de clase: {', '.join(types)}", color=ft.colors.WHITE))
            message.value = ""  # Limpiar mensaje de error

            # Mostrar u ocultar el botón de eliminar asignatura dependiendo de si hay asignaturas en la lista
            remove_subject_button.visible = len(subjects) > 0
            page.update()

        def remove_subject():
            if subjects:
                subjects.pop()  # Elimina la última asignatura de la lista
                subject_list.controls.pop()  # Elimina la última asignatura de la vista
                message.value = "Última asignatura eliminada."
                message.color = ft.colors.GREEN

                # Mostrar u ocultar el botón de eliminar asignatura dependiendo de si hay asignaturas en la lista
                remove_subject_button.visible = len(subjects) > 0
                page.update()

        # Asignar el evento para mostrar/ocultar campos de asignaturas
        adding_subjects.on_change = toggle_subject_fields
        subject_code_input.on_change = toggle_subject_fields  # Añadir este evento

        page.add(
            ft.Column(
                [
                    ft.Text("", size=10),
                    ft.Text("Registro de Usuario", size=30),
                    ft.Text("", size=10),
                    email_input,
                    reg_username_input,
                    reg_password_input,
                    name_input,
                    surname_input,
                    degree_input,
                    register_error_text,
                    adding_subjects,  # Checkbox para agregar asignaturas
                    ft.Text("", size=10),
                    subject_code_input,
                    class_types_input,
                    message,
                    add_subject_button,
                    subject_list,
                    remove_subject_button,
                    register_button,
                    ft.TextButton("¿Ya tienes una cuenta? Inicia sesión", on_click=show_login_form),
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
        username_input = ft.TextField(label="Usuario", width=page.width)
        password_input = ft.TextField(label="Contraseña", password=True, width=page.width)
        login_button = ft.CupertinoFilledButton("Iniciar sesión", on_click=login_clicked)
        error_text = ft.Text(color="red")

        page.add(
            ft.Column(
                [   
                    ft.Text("", size=10),
                    ft.Text("Iniciar sesión", size=30),
                    ft.Text("", size=10),
                    username_input,
                    password_input,
                    ft.Text("", size=10),
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

    page.scroll = "always"

    # Si no está autenticado, mostrar el formulario de inicio de sesión
    if not authenticated:
        show_login_form()
    else:
        show_main_view()


# Ejecutar la app
ft.app(target=main)