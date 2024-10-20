import flet as ft

class Agenda(ft.UserControl):
    def build(self):
        return ft.Column([
            ft.Text("Agenda", size=30),
            ft.Text("Aquí puedes ver tu agenda."),
        ])
