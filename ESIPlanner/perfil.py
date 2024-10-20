import flet as ft

class Perfil(ft.UserControl):
    def build(self):
        return ft.Column([
            ft.Text("Perfil", size=30),
            ft.Text("Aquí puedes ver tu perfil."),
        ])
