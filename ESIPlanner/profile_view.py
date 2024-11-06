import flet as ft

class Profile(ft.View):
    def __init__(self, username, on_logout):
        super().__init__()
        self.username = username  # Guardar el nombre de usuario
        self.on_logout = on_logout  # Función para cerrar sesión
        self.content = self.build()

    def build(self):
        return ft.Column(
            [
                ft.Text(f"Perfil de {self.username}", size=30),  # Mostrar el nombre de usuario
                # Botón para cerrar sesión
                ft.ElevatedButton("Cerrar sesión", on_click=self.logout),
            ]
        )

    def logout(self, e):
        # Llamar a la función de cierre de sesión pasada como parámetro
        self.on_logout(e)
