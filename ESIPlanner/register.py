import flet as ft

class Register(ft.UserControl):
    def __init__(self, page: ft.Page, change_view, on_register_success):
        super().__init__()
        self.page = page
        self.change_view = change_view
        self.on_register_success = on_register_success

    def build(self):
        return ft.Column(
            [
                ft.TextField(label="Username"),
                ft.TextField(label="Email"),
                ft.TextField(label="Password", password=True),
                ft.ElevatedButton("Register", on_click=self.register),
                ft.TextButton("Ya tienes cuenta? Inicia sesión", on_click=self.login),
            ]
        )

    def register(self, e):
        # Aquí iría la lógica de registro
        self.on_register_success()  # Llamada a la función si el registro es exitoso

    def login(self, e):
        self.change_view(0)  # Cambia a la vista de inicio de sesión
