import flet as ft

class Profile(ft.View):
    def __init__(self, username):
        super().__init__()
        self.username = username  # Guardar el nombre de usuario
        self.content = self.build()

    def build(self):
        return ft.Column(
            [
                ft.Text(f"Perfil de {self.username}", size=30),  # Mostrar el nombre de usuario
                # Aquí puedes agregar más contenido para el perfil
            ]
        )
