# agenda_view.py
import flet as ft

class Agenda(ft.View):
    def __init__(self):
        super().__init__()
        self.content = self.build()

    def build(self):
        print ("BUILD AGENDA")
        return ft.Column([
            ft.Text("", size=10),
            ft.Text("Agenda", size=30),
            ft.Text("Esta es la vista de la agenda."),
        ])
