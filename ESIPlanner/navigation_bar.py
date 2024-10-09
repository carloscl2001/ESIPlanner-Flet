# navigation_bar.py
import flet as ft

class NavigationBarComponent:
    def __init__(self):
        self.navigation_bar = ft.NavigationBar(
            adaptive=True,
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.icons.HOME_ROUNDED,  # Icono blanco 
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
            bgcolor="#26272B",  # Fondo oscuro

            
        )

    def get_navigation_bar(self):
        return self.navigation_bar