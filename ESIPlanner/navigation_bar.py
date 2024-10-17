# navigation_bar.py
import flet as ft

class NavigationBarComponent:
    def __init__(self, on_destination_change):
        # NavigationBar con un evento on_change para capturar selecciones
        self.navigation_bar = ft.NavigationBar(
            adaptive=True,
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.icons.HOME_ROUNDED,
                    label="Home"
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.CALENDAR_MONTH_OUTLINED,
                    label="Agenda"
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.CALENDAR_VIEW_WEEK,
                    label="Horario"
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.PERSON_ROUNDED,
                    label="Perfil"
                ),
            ],
            bgcolor="#26272B",
            on_change=on_destination_change  # Se llama cuando el destino cambia
        )

    def get_navigation_bar(self):
        return self.navigation_bar
# navigation_bar.py
import flet as ft

class NavigationBarComponent:
    def __init__(self, on_destination_change):
        # NavigationBar con un evento on_change para capturar selecciones
        self.navigation_bar = ft.NavigationBar(
            adaptive=True,
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.icons.HOME_ROUNDED,
                    label="Home"
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.CALENDAR_MONTH_OUTLINED,
                    label="Agenda"
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.CALENDAR_VIEW_WEEK,
                    label="Horario"
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.PERSON_ROUNDED,
                    label="Perfil"
                ),
            ],
            bgcolor="#26272B",
            on_change=on_destination_change  # Se llama cuando el destino cambia
        )

    def get_navigation_bar(self):
        return self.navigation_bar
