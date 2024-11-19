import datetime
import flet as ft

class Timetable(ft.View):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.selected_date_text = ft.Text("")  # Elemento de texto para mostrar la fecha seleccionada
        self.content = self.build()

    def build(self):
        print("BUILD AGENDA")
        
        return ft.Column([
            ft.Text("", size=10),
            ft.Text("Agenda", size=30),
            ft.Text("Esta es la vista de la agenda."),
            
            # Botón para abrir el DatePicker
            ft.ElevatedButton(
                "Selecciona un día",
                icon=ft.icons.CALENDAR_MONTH,
                on_click=self.open_date_picker  # Llama al DatePicker al hacer clic
            ),
            
            # Texto para mostrar la fecha seleccionada en pantalla
            self.selected_date_text,
        ], spacing=10)

    def open_date_picker(self, e):
        # Crear y abrir el DatePicker
        e.page.open(
            ft.DatePicker(
                first_date=datetime.datetime(year=2023, month=1, day=1),
                last_date=datetime.datetime(year=2024, month=12, day=31),
                on_change=self.on_date_selected,
                on_dismiss=self.on_date_picker_dismissed
            )
        )

    def on_date_selected(self, e):
        # Actualizar el texto con la fecha seleccionada y mostrarlo en pantalla
        selected_date = e.control.value.strftime('%Y-%m-%d')
        self.selected_date_text.value = f"Día seleccionado: {selected_date}"
        self.selected_date_text.update()  # Actualizar solo el control específico del texto

    def on_date_picker_dismissed(self, e):
        # Manejar el caso en el que se cierra el DatePicker sin seleccionar una fecha
        print("DatePicker cerrado sin seleccionar una fecha.")
