import flet as ft

class Login(ft.UserControl):
    def __init__(self, on_success):
        super().__init__()
        self.on_success = on_success

    def build(self):
        return ft.Column([
            ft.Text("Login", size=30),
            ft.TextField(label="Username"),
            ft.TextField(label="Password", password=True),
            ft.ElevatedButton(text="Login", on_click=self.handle_login)
        ])

    def handle_login(self, e):
        # Aquí deberías validar las credenciales
        # Si las credenciales son correctas:
        self.on_success()  # Llamar a la función de éxito en login
