import flet as ft

class Horario(ft.UserControl):
    def build(self):
        return ft.Column([
            ft.Text("Horario", size=30),
            ft.Text("Aquí puedes ver tu horario."),
        ])
