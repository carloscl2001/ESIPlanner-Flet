import flet as ft

class Login(ft.UserControl):
    def __init__(self, page: ft.Page, change_view, on_login_success):
        super().__init__()
        self.page = page
        self.change_view = change_view
        self.on_login_success = on_login_success

    def build(self):
        return ft.Column(
            [
                ft.TextField(label="Username"),
                ft.TextField(label="Password", password=True),
                ft.ElevatedButton("Login", on_click=self.login),
                ft.TextButton("No tienes cuenta? Regístrate", on_click=self.register),
            ]
        )

    def login(self, e):
        # Aquí iría la lógica de autenticación
        self.on_login_success()  # Llamada a la función si el login es exitoso

    def register(self, e):
        self.change_view(1)  # Cambia a la vista de registro
