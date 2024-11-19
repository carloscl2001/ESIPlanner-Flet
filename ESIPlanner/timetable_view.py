import flet as ft
import requests
from datetime import datetime, timedelta

class Timetable(ft.View):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.subjects_data = None
        self.selected_date_text = ft.Text("")  # Elemento de texto para mostrar la fecha seleccionada
        self.week_classes = []  # Lista para almacenar las clases de la semana
        self.column = None
        self.content = self.build()

    def build(self):
        self.column = ft.Column([
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
        
        return self.column

    def open_date_picker(self, e):
        print("Abriendo DatePicker...")  # Depuración
        # Crear y abrir el DatePicker
        e.page.open(
            ft.DatePicker(
                first_date=datetime(year=2023, month=1, day=1),
                last_date=datetime(year=2024, month=12, day=31),
                on_change=self.on_date_selected,
                on_dismiss=self.on_date_picker_dismissed
            )
        )

    def load_classes_of_week(self, start_of_week, end_of_week):
        print(f"Cargando clases de la semana desde {start_of_week} hasta {end_of_week}...")  # Depuración
        # Aquí puedes agregar la lógica de carga de clases, por ejemplo:
        self.load_user_subjects(start_of_week, end_of_week)

    def on_date_selected(self, e):
        # Obtener el día seleccionado y calcular la semana
        selected_date = e.control.value.date()
        self.selected_date_text.value = f"Día seleccionado: {selected_date.strftime('%Y-%m-%d')}"
        self.selected_date_text.update()

        print(f"Día seleccionado: {selected_date}")  # Depuración

        # Calcular los días de la semana (Lunes a Viernes)
        start_of_week = selected_date - timedelta(days=selected_date.weekday())
        end_of_week = start_of_week + timedelta(days=4)


        # Llamar a la función para cargar las clases de esa semana
        self.load_classes_of_week(start_of_week, end_of_week)

    def on_date_picker_dismissed(self, e):
        # Manejar el caso en que se cierra el DatePicker sin seleccionar una fecha
        print("DatePicker cerrado sin seleccionar una fecha.")

    def load_user_subjects(self, start_of_week, end_of_week):
        try:
            print(f"Cargando asignaturas para el usuario: {self.username}...")  # Depuración
            response = requests.get(f"http://127.0.0.1:8000/users/{self.username}/subjects")
            if response.status_code == 200:
                self.subjects_data = response.json()
                print(f"Datos de asignaturas recibidos: {self.subjects_data}")  # Depuración

                # Verificar si hay asignaturas vinculadas al perfil
                if not self.subjects_data:
                    # Si no hay asignaturas, mostrar mensaje en la pantalla
                    self.column.controls.append(ft.Text("No tienes asignaturas vinculadas a tu perfil.", size=16, color="red"))
                else:
                    # Recopilar clases de todas las asignaturas y añadirlas a week_classes
                    for subject in self.subjects_data:
                        # Pasar start_of_week y end_of_week a la función load_class_data
                        self.load_class_data(subject['code'], subject['types'], start_of_week, end_of_week)
                    # Actualizar la interfaz después de procesar todas las asignaturas
                    print("Vamos a actualizar")
                    self.update_classes_data(self.week_classes)
            else:
                print(f"Error en la solicitud: {response.status_code}")
        except Exception as e:
            print(f"Error al obtener las asignaturas: {e}")

    def load_class_data(self, subject_code, user_types, start_of_week, end_of_week):
        print(f"Cargando datos de clase para la asignatura con código {subject_code}...")  # Depuración
        try:
            response = requests.get(f"http://127.0.0.1:8000/subjects/{subject_code}")
            if response.status_code == 200:
                class_data = response.json()
                #print(f"Datos de clase recibidos para {subject_code}: {class_data}")  # Depuración
                # Filtrar las clases de esta semana que corresponden al tipo del usuario
                week_classes = self.filter_classes_this_week(class_data, user_types, start_of_week, end_of_week)
                # Añadir las clases filtradas a la lista principal week_classes
                self.week_classes.extend(week_classes)
            else:
                print(f"Error en la solicitud para el código {subject_code}: {response.status_code}")
        except Exception as e:
            print(f"Error al obtener las clases para el código {subject_code}: {e}")

    def filter_classes_this_week(self, class_data, user_types, start_of_week, end_of_week):
        print(f"Filtrando clases para esta semana...")  # Depuración
        
        
        week_classes = []
        for class_info in class_data['classes']:
            if class_info['type'] in user_types:  # Solo incluir clases del tipo correspondiente al usuario
                for event in class_info['events']:
                    try:
                        class_date = datetime.strptime(event['date'], "%Y-%m-%d").date()
                        if start_of_week <= class_date <= end_of_week:
                            week_classes.append({
                                'code': class_data['code'],
                                'name': class_data['name'],
                                'class_type': class_info['type'],
                                'event_date': class_date,
                                'start_hour': event['start_hour'],
                                'end_hour': event['end_hour'],
                                'location': event['location']
                            })
                    except ValueError as ve:
                        print(f"Error al convertir la fecha de la clase: {event['date']} - {ve}")
        print(f"Filtrando clases para esta semana ACABADO...")  # Depuración
        return week_classes

    def update_classes_data(self, week_classes):
        print(f"Semana de clases: {self.week_classes}")  # Verifica si la lista tiene datos
        if not self.week_classes:

            # Si no hay clases, mostrar el mensaje de "no tienes clase"
            self.column.controls.append(ft.Text("Esta semana no tienes clase.", size=16, color="red"))
        else:
            print("--------------------------------------------------------------------------------------------------------------------------")
            print("HAY CLASES")
            days_of_week = {0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves', 4: 'Viernes'}
            grouped_by_day = {day: [] for day in days_of_week.values()}

            print("--------------------------------------------------------------------------------------------------------------------------")
            print("ENTRA PRIMER FOR")
            for class_info in self.week_classes:
                day_of_week = class_info['event_date'].weekday()
                if day_of_week < 5:
                    day_name = days_of_week[day_of_week]
                    grouped_by_day[day_name].append(class_info)

            print("--------------------------------------------------------------------------------------------------------------------------")
            print("ENTRA SEGUNDO FOR")
            # Mostrar las clases con estilo
            for day, classes in grouped_by_day.items():
                if classes:
                    # Añadir encabezado del día
                    self.column.controls.append(ft.Text(day, size=20, weight="bold", color="teal700"))
                    
                    # Ordenar clases por hora de inicio
                    classes.sort(key=lambda x: x['start_hour'])

                    # Crear tarjetas para cada clase
                    for class_info in classes:
                        # Determinar la descripción del tipo de clase según la letra inicial
                        class_type_description = self.get_class_type_description(class_info['class_type'])

                        class_card = ft.Container(
                            content=ft.Column([ft.Text(f"{class_info['name']}", size=18, weight="bold", color="black"),
                                               ft.Text(f"{class_info['class_type']} - {class_type_description}", size=14, color="black"),
                                               ft.Text(f"Hora: {class_info['start_hour']} - {class_info['end_hour']}", size=14, color="black"),
                                               ft.Text(f"Ubicación: {class_info['location']}", size=14, color="black"),
                                               ], spacing=5),
                            padding=10,
                            border=ft.border.all(3, color="gray"),
                            border_radius=ft.border_radius.all(8),
                            margin=ft.margin.only(right=15, bottom=8),  # Añade margen derecho para evitar solapamiento con el scroll
                            bgcolor="white",
                            expand=True
                        )
                        self.column.controls.append(class_card)
            print("--------------------------------------------------------------------------------------------------------------------------")
            print("SALE SEGUNDO FOR")

        self.update()

    def get_class_type_description(self, class_type):
        """Devuelve la descripción correspondiente según la primera letra del tipo de clase."""
        type_descriptions = {
            'A': 'Clases de teoría',
            'B': 'Clases de problemas',
            'C': 'Clases de prácticas',
            'D': 'Prácticas de laboratorio',
            'X': 'Clases teórico-prácticas'
        }
        # Tomar solo la primera letra del tipo de clase
        class_letter = class_type[0] if class_type else ''
        return type_descriptions.get(class_letter, 'Tipo desconocido')
