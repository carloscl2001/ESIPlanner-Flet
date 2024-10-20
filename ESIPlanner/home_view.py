# home_view.py
import flet as ft

class Home(ft.View):
    def __init__(self):
        super().__init__()
        self.content = self.build()

    def build(self):
        return ft.Column([
            ft.Text("Bienvenido a la página de inicio", size=30),
            ft.Text("Esta es la vista principal."),
        ])
