# profile_view.py
import flet as ft

class Profile(ft.View):
    def __init__(self):
        super().__init__()
        self.content = self.build()

    def build(self):
        return ft.Column([
            ft.Text("Perfil", size=30),
            ft.Text("Esta es la vista del perfil."),
        ])
