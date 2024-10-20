import flet as ft

class Timetable(ft.View):
    def __init__(self):
        super().__init__()
        self.content = self.build()
        
    def build(self):
        return ft.Column([
            ft.Text("Horario", size=30),
            ft.Text("Aquí puedes ver tu horario."),
        ])
