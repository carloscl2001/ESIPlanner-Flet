import flet as ft
import requests

class Profile(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.content = self.build()

    def build(self):
        return ft.Column([
            ft.Text("Perfil", size=30),
            ft.Text("Aquí puedes ver tu perfil."),
        ])
