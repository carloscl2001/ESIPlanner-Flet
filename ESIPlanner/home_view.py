# home_view.py
import flet as ft

class Home(ft.View):
    def __init__(self):
        super().__init__()
        self.content = self.build()

    def build(self):
        print ("BUILD HOME")
        return ft.Column([
            ft.Text("", size=10),
            ft.Text("Bienvenido a la página de inicio", size=30),
            ft.Text("Esta es la vista principal."),
        ])
