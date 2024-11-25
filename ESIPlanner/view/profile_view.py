import flet as ft
import requests

class Profile(ft.View):
    def __init__(self, username, on_logout):
        super().__init__()
        self.username = username
        self.on_logout = on_logout
        self.user_data = None  # Inicializamos con None
        self.column = None  # Definir la columna fuera de `build`
        self.content = self.build()

    def build(self):
        # Crear la columna con los controles iniciales
        self.column = ft.Column([
            ft.Text(f"Perfil de {self.username}", size=30),  # Título de la vista
            ft.ElevatedButton("Cerrar sesión", on_click=self.logout),
            ft.Text("Cargando datos...")  # Inicialmente mostramos el mensaje de carga
        ])
        
        # Llamamos a la función para obtener los datos del usuario
        self.load_user_data()

        return self.column

    def load_user_data(self):
        # Realizar la petición para obtener los datos del usuario en un hilo separado
        try:
            response = requests.get(f"http://127.0.0.1:8000/users/{self.username}")
            if response.status_code == 200:  # Verificar si la respuesta es exitosa
                user_data = response.json()
                self.user_data = user_data
                #print(f"Datos del usuario obtenidos: {self.user_data}")
                
                # Llamar a `update` después de obtener los datos
                self.update_user_data()
            else:
                print(f"Error en la solicitud: {response.status_code}")
        except Exception as e:
            print(f"Error al obtener los datos del usuario: {e}")

    def update_user_data(self):
        # Limpiar el mensaje de carga y agregar los datos del usuario
        self.column.controls = [
            ft.Text("", size=10),
            ft.Text(f"{self.username}", size=30),
            ft.Text(f"Usuario: {self.user_data['username']}"),
            ft.Text(f"Nombre: {self.user_data['name']}"),
            ft.Text(f"Apellidos: {self.user_data['surname']}"),
            ft.Text(f"Email: {self.user_data['email']}"),
            ft.Text(f"Grado: {self.user_data['degree']}"),
            ft.ElevatedButton("Cerrar sesión", on_click=self.logout),
        ]

        # Mostrar las asignaturas
        if self.user_data['subjects']:
            subjects_text = "\n".join([f"Asignaturas: {sub['code']} - Grupos: {', '.join(sub['types'])}" for sub in self.user_data['subjects']])
            self.column.controls.append(ft.Text(f"Tus asignaturas: \n{subjects_text}"))
        else:
            self.column.controls.append(ft.Text("No tiene asignaturas asignadas"))
        
        # Actualizar la interfaz
        self.update()

    def logout(self, e):
        # Llamar a la función de cierre de sesión
        self.on_logout(e)
