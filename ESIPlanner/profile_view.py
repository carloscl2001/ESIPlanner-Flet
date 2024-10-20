import flet as ft

class Profile(ft.UserControl):
    def __init__(self):
        self.content = self.build()\
        
    def build(self):
        return ft.Column([
            ft.Text("Perfil", size=30),
            ft.Text("Aqui puedes ver tu perfil."),
        ])
