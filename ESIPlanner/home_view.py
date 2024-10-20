import flet as ft

class Home:
    def __init__(self):
        self.content = self.build()

    def build(self):
        return ft.Column([
            ft.Text("Bienvenido a la página de inicio", size=30),
            ft.Text("Esta es la vista principal."),
        ])
