import flet as ft
import requests
from datetime import datetime, timedelta

class Home(ft.View):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.subjects_data = None
        self.week_classes = []  # Lista para almacenar todas las clases de la semana de todas las asignaturas
        self.column = None
        self.content = self.build()

    def build(self):
        self.column = ft.Column([
            ft.Text("",size=10),
            ft.Text("Tus clases esta semana", size=30, weight="bold", color="#0757fa"),
            ft.Text("", size=5),  # Espaciado entre el título y el mensaje
        ], spacing=10)

        # Llamar a la función para cargar las asignaturas del usuario
        self.load_user_subjects()

        return self.column

    def load_user_subjects(self):
        try:
            response = requests.get(f"http://127.0.0.1:8000/users/{self.username}/subjects")
            if response.status_code == 200:
                self.subjects_data = response.json()
                # Verificar si hay asignaturas vinculadas al perfil
                if not self.subjects_data:
                    # Si no hay asignaturas, mostrar mensaje en la pantalla
                    self.column.controls.append(ft.Text("No tienes asignaturas vinculadas a tu perfil.", size=16, color="red"))
                else:
                    # Recopilar clases de todas las asignaturas y añadirlas a week_classes
                    for subject in self.subjects_data:
                        self.load_class_data(subject['code'], subject['types'])
                    # Actualizar la interfaz después de procesar todas las asignaturas
                    self.update_classes_data(self.week_classes)
            else:
                print(f"Error en la solicitud: {response.status_code}")
        except Exception as e:
            print(f"Error al obtener las asignaturas: {e}")

    def load_class_data(self, subject_code, user_types):
        try:
            response = requests.get(f"http://127.0.0.1:8000/subjects/{subject_code}")
            if response.status_code == 200:
                class_data = response.json()
                # Filtrar las clases de esta semana que corresponden al tipo del usuario
                week_classes = self.filter_classes_this_week(class_data, user_types)
                # Añadir las clases filtradas a la lista principal week_classes
                self.week_classes.extend(week_classes)
            else:
                print(f"Error en la solicitud para el código {subject_code}: {response.status_code}")
        except Exception as e:
            print(f"Error al obtener las clases para el código {subject_code}: {e}")

    def filter_classes_this_week(self, class_data, user_types):
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=4)
        start_of_week = start_of_week.date()
        end_of_week = end_of_week.date()

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

        return week_classes
    def update_classes_data(self, week_classes):
        if not week_classes:
            # Si no hay clases, mostrar el mensaje de "no tienes clase"
            self.column.controls.append(ft.Text("Esta semana no tienes clase.", size=16, color="red"))
        else:
            days_of_week = {0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves', 4: 'Viernes'}
            grouped_by_day = {day: [] for day in days_of_week.values()}

            for class_info in week_classes:
                day_of_week = class_info['event_date'].weekday()
                if day_of_week < 5:
                    day_name = days_of_week[day_of_week]
                    grouped_by_day[day_name].append(class_info)

            # Mostrar las clases con estilo
            for day, classes in grouped_by_day.items():
                if classes:
                    # Añadir encabezado del día
                    self.column.controls.append(ft.Text(day, size=20, weight="bold", color="teal700"))
                    
                    # Ordenar clases por hora de inicio
                    classes.sort(key=lambda x: x['start_hour'])

                    # Detectar solapamientos
                    overlapping_classes = self.detect_overlapping_classes(classes)

                    # Crear tarjetas para cada clase
                    for class_info in classes:
                        # Determinar la descripción del tipo de clase según la letra inicial
                        class_type_description = self.get_class_type_description(class_info['class_type'])

                        # Verificar si esta clase está en solapamiento
                        is_overlapping = any(oc['code'] == class_info['code'] and
                                            oc['start_hour'] == class_info['start_hour'] for oc in overlapping_classes)

                        # Definir el color de fondo según si hay solapamiento
                        bgcolor = "yellow" if is_overlapping else "white"

                        class_card = ft.Container(
                            content=ft.Column([
                                ft.Text(f"{class_info['name']}", size=18, weight="bold", color="black"),
                                ft.Text(f"{class_info['class_type']} - {class_type_description}", size=14, color="black"),
                                ft.Text(f"Hora: {class_info['start_hour']} - {class_info['end_hour']}", size=14, color="black"),
                                ft.Text(f"Ubicación: {class_info['location']}", size=14, color="black"),
                            ], spacing=5),
                            padding=10,
                            border=ft.border.all(3, color="gray"),
                            border_radius=ft.border_radius.all(8),
                            margin=ft.margin.only(right=15, bottom=8),
                            bgcolor=bgcolor,  # Color dinámico según solapamiento
                            expand=True
                        )
                        self.column.controls.append(class_card)

        self.update()

    def detect_overlapping_classes(self, classes):
        """Detecta clases que se solapan en horario."""
        overlapping = []
        for i in range(len(classes)):
            for j in range(i + 1, len(classes)):
                class_a = classes[i]
                class_b = classes[j]

                # Convertir horas a formato datetime para compararlas
                start_a = datetime.strptime(class_a['start_hour'], "%H:%M")
                end_a = datetime.strptime(class_a['end_hour'], "%H:%M")
                start_b = datetime.strptime(class_b['start_hour'], "%H:%M")
                end_b = datetime.strptime(class_b['end_hour'], "%H:%M")

                # Verificar si hay solapamiento
                if start_a < end_b and start_b < end_a:
                    if class_a not in overlapping:
                        overlapping.append(class_a)
                    if class_b not in overlapping:
                        overlapping.append(class_b)
        return overlapping


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
