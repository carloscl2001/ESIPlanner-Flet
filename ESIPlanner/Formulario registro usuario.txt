import flet as ft
import requests

def main(page: ft.Page):
    page.title = "Formulario de Registro"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.bgcolor = ft.colors.WHITE  # Fondo de la página blanco
    
    # Contenedor con fondo azul claro
    form_container = ft.Container(
        bgcolor="#e3e9ff",  # Color de fondo azul claro
        padding=20,
        border_radius=10,
        width=page.width,  # Ocupar el ancho completo de la página
    )

    # Definición de controles del formulario
    email_input = ft.TextField(label="Email", width=page.width, bgcolor="#e3e9ff", color=ft.colors.BLACK)
    username_input = ft.TextField(label="Username", width=page.width, bgcolor="#e3e9ff", color=ft.colors.BLACK)
    name_input = ft.TextField(label="Nombre", width=page.width, bgcolor="#e3e9ff", color=ft.colors.BLACK)
    surname_input = ft.TextField(label="Apellido", width=page.width, bgcolor="#e3e9ff", color=ft.colors.BLACK)
    degree_input = ft.TextField(label="Grado", width=page.width, bgcolor="#e3e9ff", color=ft.colors.BLACK)

    subjects = []
    adding_subjects = ft.Checkbox(label="¿Quieres añadir asignaturas?", value=False, active_color=ft.colors.BLACK)  # Checkbox para agregar asignaturas
    message = ft.Text("")  # Mensaje de éxito o error

    # Controles para agregar asignaturas (inicialmente ocultos)
    subject_code_input = ft.TextField(label="Código de asignatura", width=page.width, bgcolor="#e3e9ff", color=ft.colors.BLACK, visible=False)
    class_types_input = ft.TextField(label="Tipos de clase (separadas por comas)", width=page.width, bgcolor="#e3e9ff", color=ft.colors.BLACK, visible=False)
    add_subject_button = ft.ElevatedButton("Agregar Asignatura", on_click=lambda e: add_subject(), visible=False)

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

        # Validar que haya al menos un tipo de clase y un código de asignatura
        if code and types and len(types) > 0:
            subjects.append({"code": code, "types": [type.strip() for type in types]})
            subject_code_input.value = ""
            class_types_input.value = ""
            subject_list.controls.append(ft.Text(f"Código: {code}, Tipos: {', '.join(types)}", color=ft.colors.BLACK))
            page.update()
        else:
            if not code:
                message.value = "Debes ingresar un código de asignatura."
                subject_code_input.focused = True
                subject_code_input.border_color = ft.colors.RED
            else:
                subject_code_input.border_color = ft.colors.BLUE  # Resetear color
            if len(types) == 0:
                message.value = "Debes ingresar al menos un tipo de clase."
                class_types_input.focused = True
                class_types_input.border_color = ft.colors.RED
            else:
                class_types_input.border_color = ft.colors.BLUE  # Resetear color
            message.color = ft.colors.RED
            page.update()

    def submit_form(e):
        # Limpiar el mensaje anterior
        message.value = ""

        # Validar campos obligatorios
        required_fields = [
            (email_input, "Email"),
            (username_input, "Username"),
            (name_input, "Nombre"),
            (surname_input, "Apellido"),
            (degree_input, "Grado")
        ]

        missing_fields = []

        for field, label in required_fields:
            if not field.value:
                field.border_color = ft.colors.RED
                missing_fields.append(label)
            else:
                field.border_color = ft.colors.BLUE  # Resetear color

        if missing_fields:
            message.value = f"Por favor, completa los siguientes campos: {', '.join(missing_fields)}."
            message.color = ft.colors.RED
            page.update()
            return

        # Validar asignaturas si se ha seleccionado añadir
        if adding_subjects.value and not subjects:
            message.value = "Por favor, añade al menos una asignatura."
            message.color = ft.colors.RED
            page.update()
            return
        
        # Validar tipo de clases si se ha añadido alguna asignatura
        for subject in subjects:
            if not subject["types"]:
                message.value = "Por favor, añade al menos un tipo de clase para cada asignatura."
                message.color = ft.colors.RED
                page.update()
                return

        data = {
            "email": email_input.value,
            "username": username_input.value,
            "name": name_input.value,
            "surname": surname_input.value,
            "degree": degree_input.value,
            "subjects": subjects,
        }
        
        # Realizar la solicitud POST
        response = requests.post("http://127.0.0.1:8000/users/", json=data)
        
        if response.status_code == 201:  # Asumiendo que el servidor responde con 201 si se crea correctamente
            message.value = "Formulario enviado correctamente!"
            message.color = ft.colors.GREEN  # Color para mensaje de éxito
        else:
            message.value = "Error al enviar el formulario."
            message.color = ft.colors.RED  # Color para mensaje de error

        # Limpiar los campos del formulario
        for control in [email_input, username_input, name_input, surname_input, degree_input]:
            control.value = ""
        subjects.clear()
        subject_list.controls.clear()
        adding_subjects.value = False  # Resetear el checkbox
        toggle_subject_fields(None)  # Ocultar campos de asignaturas
        page.update()

    # Asignar el evento para mostrar/ocultar campos de asignaturas
    adding_subjects.on_change = toggle_subject_fields
    subject_code_input.on_change = toggle_subject_fields  # Añadir este evento

    submit_button = ft.ElevatedButton("Enviar", on_click=submit_form)

    # Organizar controles en el contenedor
    form_container.content = ft.Column(controls=[
        email_input,
        username_input,
        name_input,
        surname_input,
        degree_input,
        adding_subjects,  # Checkbox para agregar asignaturas
        subject_code_input,
        class_types_input,
        add_subject_button,
        subject_list,
        submit_button,
        message  # Mensaje debajo del botón de enviar
    ])

    # Agregar el contenedor a la página
    page.add(form_container)

ft.app(target=main)
