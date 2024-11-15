import flet as ft
import requests
from datetime import datetime, timedelta

class Home(ft.View):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.subjects_data = None  # Inicializamos con None
        self.column = None  # Definir la columna fuera de `build`
        self.content = self.build()

    def build(self):
        # Crear la columna con los controles iniciales
        self.column = ft.Column([
            ft.Text(f"Tus clases esta semana", size=30),  # Título de la vista
        ])
        
        # Llamamos a la función para obtener las asignaturas del usuario
        self.load_user_subjects()

        return self.column

    def load_user_subjects(self):
        # Realizar la petición para obtener las asignaturas del usuario
        try:
            response = requests.get(f"http://127.0.0.1:8000/users/{self.username}/subjects")
            if response.status_code == 200:  # Verificar si la respuesta es exitosa
                subjects_data = response.json()
                self.subjects_data = subjects_data
                # Realizar peticiones para obtener las clases de cada asignatura
                for subject in self.subjects_data:
                    self.load_class_data(subject['code'])  # Llamada a la función para obtener las clases de cada asignatura
            else:
                print(f"Error en la solicitud: {response.status_code}")
        except Exception as e:
            print(f"Error al obtener las asignaturas: {e}")

    def load_class_data(self, subject_code):
        # Realizar una petición para obtener las clases de la asignatura
        try:
            response = requests.get(f"http://127.0.0.1:8000/subjects/{subject_code}")
            if response.status_code == 200:  # Verificar si la respuesta es exitosa
                class_data = response.json()
                # Filtrar las clases que corresponden a esta semana
                week_classes = self.filter_classes_this_week(class_data)
                # Mostrar las clases de esta semana en la columna
                self.update_classes_data(week_classes)
            else:
                print(f"Error en la solicitud para el código {subject_code}: {response.status_code}")
        except Exception as e:
            print(f"Error al obtener las clases para el código {subject_code}: {e}")

    def filter_classes_this_week(self, class_data):
        print("Ejecutando la función filter_classes_this_week...")

        # Obtener las fechas de la semana actual
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())  # Lunes de esta semana
        end_of_week = start_of_week + timedelta(days=4)  # Viernes de esta semana (no incluir sábados ni domingos)

        # Asegurarse de comparar solo la fecha sin las horas
        start_of_week = start_of_week.date()
        end_of_week = end_of_week.date()

        print(f"start_of_week: {start_of_week}, end_of_week: {end_of_week}")

        # Filtrar las clases que estén dentro de esta semana (lunes a viernes)
        week_classes = []

        # Iterar sobre las clases de cada asignatura
        for class_info in class_data['classes']:
            # Iterar sobre los eventos de cada clase
            for event in class_info['events']:
                print(f"Procesando evento para clase {class_info['type']}, fecha: {event['date']}")

                try:
                    # Asegurarnos de que la fecha esté en formato "YYYY-MM-DD"
                    class_date = datetime.strptime(event['date'], "%Y-%m-%d").date()  # Obtener solo la fecha (sin hora)
                    print(f"Fecha de clase convertida: {class_date}")

                    # Verificar si la clase está dentro de esta semana (lunes a viernes)
                    if start_of_week <= class_date <= end_of_week:
                        print(f"Clase {class_info['type']} está dentro de esta semana.")
                        # Añadir el evento a la lista de clases de esta semana
                        week_classes.append({
                            'code': class_data['code'],  # Código de la asignatura
                            'name': class_data['name'],  # Nombre de la asignatura
                            'class_type': class_info['type'],  # Tipo de clase (A1, C1, C2)
                            'event_date': class_date,
                            'start_hour': event['start_hour'],
                            'end_hour': event['end_hour'],
                            'location': event['location']
                        })
                    else:
                        print(f"La clase {class_info['type']} NO está dentro de esta semana. Fecha: {class_date}")
                except ValueError as ve:
                    print(f"Error al convertir la fecha de la clase: {event['date']} - {ve}")

        if not week_classes:
            print("No se encontraron clases para esta semana.")
        else:
            print(f"Clases de esta semana: {week_classes}")

        print("FIN DE EJECUCION DE la función filter_classes_this_week...")

        return week_classes


    def update_classes_data(self, week_classes):
        # Crear un diccionario para agrupar las clases por día (solo lunes a viernes)
        days_of_week = {0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves', 4: 'Viernes'}
        grouped_by_day = {day: [] for day in days_of_week.values()}
        
        # Agrupar las clases por día
        for class_info in week_classes:
            day_of_week = class_info['event_date'].weekday()  # Obtener el día de la semana (0-6)
            if day_of_week < 5:  # Asegurarse de que solo incluimos lunes a viernes
                day_name = days_of_week[day_of_week]
                grouped_by_day[day_name].append(class_info)

        # Mostrar las clases en la interfaz, organizadas por día y hora
        subjects_text = "Clases de esta semana:\n"
        for day, classes in grouped_by_day.items():
            if classes:
                subjects_text += f"\n{day}:\n"
                # Ordenar las clases por hora de inicio
                classes.sort(key=lambda x: x['start_hour'])
                for class_info in classes:
                    subjects_text += (f"  - {class_info['name']} (Código: {class_info['code']}, Tipo: {class_info['class_type']})\n"
                                      f"    Fecha: {class_info['event_date'].strftime('%Y-%m-%d')}, "
                                      f"Hora inicio: {class_info['start_hour']} - Hora fin: {class_info['end_hour']}, "
                                      f"Ubicación: {class_info['location']}\n")
            else:
                subjects_text += f"\n{day}: No tienes clases\n"

        # Añadir el texto a la columna
        self.column.controls.append(ft.Text(subjects_text))

        # Actualizar la interfaz
        self.update()
