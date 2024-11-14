import flet as ft
import requests

class Profile(ft.View):
    def __init__(self, username, on_logout):
        super().__init__()
        self.username = username
        self.on_logout = on_logout
        self.user_data = None  # Inicializamos con None
        self.content = self.build()

    def build(self):
        # Controles iniciales de la vista
        column = ft.Column([
            ft.Text(f"Perfil de {self.username}", size=30),  # Título de la vista
            ft.ElevatedButton("Cerrar sesión", on_click=self.logout),
        ])

        # Realizar la petición para obtener los datos del usuario
        try:
            response = requests.get(f"http://127.0.0.1:8000/users/{self.username}")
            if response.status_code == 200:  # Verificar si la respuesta es exitosa
                user_data = response.json()

                # Almacenamos los datos del usuario
                self.user_data = user_data
                print(f"Datos del usuario obtenidos: {self.user_data}")

                # Actualizamos la vista
                self.update()  # Actualiza la vista para reflejar los nuevos datos
            else:
                print(f"Error en la solicitud: {response.status_code}")
        except Exception as e:
            print(f"Error al obtener los datos del usuario: {e}")

        # Aquí mostramos un mensaje de carga si los datos aún no están disponibles
        if self.user_data:
            column.controls.append(ft.Text(f"Email: {self.user_data['email']}"))
            column.controls.append(ft.Text(f"Usuario: {self.user_data['username']}"))
            column.controls.append(ft.Text(f"Nombre: {self.user_data['name']}"))
            column.controls.append(ft.Text(f"Surname: {self.user_data['surname']}"))
            column.controls.append(ft.Text(f"Degree: {self.user_data['degree']}"))

            # Mostrar las asignaturas
            subjects_text = "\n".join([f"Code: {sub['code']} - Types: {', '.join(sub['types'])}" for sub in self.user_data['subjects']])
            column.controls.append(ft.Text(f"Subjects: \n{subjects_text}"))
        else:
            # Si los datos no están disponibles, mostramos un mensaje de carga
            column.controls.append(ft.Text("Cargando datos..."))

        return column
        

    def logout(self, e):
        # Llamar a la función de cierre de sesión
        self.on_logout(e)

 