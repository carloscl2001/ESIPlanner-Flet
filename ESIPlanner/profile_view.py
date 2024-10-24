import flet as ft
import requests

class Profile(ft.UserControl):
    def __init__(self, username):
        super().__init__()
        self.username = username  # Guardar el nombre de usuario
        self.user_data = None  # Variable para almacenar los datos del usuario
        self.content = self.build()

    def build(self):
        # Hacer la petición GET para obtener los datos del usuario
        try:
            response = requests.get(f"http://127.0.0.1:8000/users/{self.username}")
            if response.status_code == 200:
                self.user_data = response.json()
            else:
                print(f"Error al obtener los datos del usuario: {response.status_code}")
        except Exception as e:
            print(f"Error al conectar con la API: {e}")

        # Verificar si se obtuvo la información correctamente
        if self.user_data:
            # Si el usuario tiene asignaturas, las mostramos; si no, mostramos un mensaje alternativo
            subjects_info = "No ha seleccionado ninguna" if not self.user_data.get('subjects') else "\n".join(
                [f"Código: {subject['code']}, Tipos: {', '.join(subject['types'])}" for subject in self.user_data['subjects']]
            )

            return ft.Column([
                ft.Text("Perfil", size=30),
                ft.Text(f"Nombre de usuario: {self.user_data['username']}"),
                ft.Text(f"Nombre: {self.user_data['name']} {self.user_data['surname']}"),
                ft.Text(f"Correo electrónico: {self.user_data['email']}"),
                ft.Text(f"Grado: {self.user_data['degree']}"),
                ft.Text(f"Asignaturas: {self.user_data['subjects']}"),
            ])
        else:
            return ft.Column([
                ft.Text("Perfil", size=30),
                ft.Text("No se pudieron obtener los datos del usuario."),
            ])
