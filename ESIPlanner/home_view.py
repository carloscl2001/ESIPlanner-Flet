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
            ft.Text("", size= 10),
            ft.Text(f"Tus clases esta semana", size=30),
        ])
        
        # Llamar a la función para cargar las asignaturas del usuario
        self.load_user_subjects()

        return self.column

    def load_user_subjects(self):
        try:
            response = requests.get(f"http://127.0.0.1:8000/users/{self.username}/subjects")
            if response.status_code == 200:
                self.subjects_data = response.json()
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
        days_of_week = {0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves', 4: 'Viernes'}
        grouped_by_day = {day: [] for day in days_of_week.values()}
        
        for class_info in week_classes:
            day_of_week = class_info['event_date'].weekday()
            if day_of_week < 5:
                day_name = days_of_week[day_of_week]
                grouped_by_day[day_name].append(class_info)

        subjects_text = ""
        for day, classes in grouped_by_day.items():
            if classes:
                subjects_text += f"\n{day}:\n"
                classes.sort(key=lambda x: x['start_hour'])
                for class_info in classes:
                    subjects_text += (
                        f"  - {class_info['name']} (Código: {class_info['code']}, Grupo: {class_info['class_type']})\n"
                        f"    Hora inicio: {class_info['start_hour']} - Hora fin: {class_info['end_hour']}, "
                        f"Ubicación: {class_info['location']}\n"
                    )

        self.column.controls.append(ft.Text(subjects_text))
        self.update()
