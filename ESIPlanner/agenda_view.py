import flet as ft


class Agenda(ft.UserControl):
    def __init__(self):
        self.content = self.build()
        
    def build(self):
        return ft.Column([
            ft.Text("Agenda", size=30),
            ft.Text("Aqui puedes ver tu agenda."),
        ])
