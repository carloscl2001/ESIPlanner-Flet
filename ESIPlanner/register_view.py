import flet as ft

class Register(ft.UserControl):
    def __init__(self, on_success):
        super().__init__()
        self.on_success = on_success  # Función a ejecutar cuando el registro sea exitoso

    def build(self):
        self.username_field = ft.TextField(label="Username", expand=True)
        self.password_field = ft.TextField(label="Password", password=True, can_reveal_password=True, expand=True)

        return ft.Column([
            ft.Text("Registro", size=30),
            self.username_field,
            self.password_field,
            ft.ElevatedButton(text="Registrarse", on_click=self.handle_register)
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def handle_register(self, e):
        username = self.username_field.value
        password = self.password_field.value

        # Aquí podrías agregar validaciones y guardar el registro en una base de datos
        if username and password:
            # Si los datos son válidos, llama a la función de éxito en el registro
            print(f"Usuario registrado: {username}")  # Mensaje de confirmación en consola
            self.on_success(username)  # Pasar el nombre de usuario a la función de éxito
        else:
            # Muestra un mensaje de error si falta algún campo
            self.page.snack_bar = ft.SnackBar(ft.Text("Por favor, rellena todos los campos"), open=True)
            self.update()
