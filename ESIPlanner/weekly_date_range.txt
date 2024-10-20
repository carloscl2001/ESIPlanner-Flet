import flet as ft
from datetime import datetime

def WeeklyDateRange(start_day, start_month, end_day, end_month, year, days_middle):
    today = datetime.today()
    
    return ft.Container(
        padding=10,
        border_radius=15,
        bgcolor='#e3e9ff',  # Fondo general del contenedor
        content=ft.Row(
            alignment="spaceEvenly",
            controls=[
                ft.Column(
                    horizontal_alignment="center",
                    controls=[
                        ft.Text(start_month, size=12, color=ft.colors.BLACK),
                        ft.Container(
                            bgcolor=ft.colors.WHITE,  # Fondo del día
                            border_radius=15,
                            padding=10,
                            content=ft.Column(  # Usar Column para alinear "Lunes" y el número
                                controls=[
                                    ft.Text("Lunes", size=12, color=ft.colors.BLACK, bgcolor = ft.colors.BLUE),  # Lunes
                                    ft.Text(
                                        str(start_day).zfill(2), 
                                        size=20, 
                                        color=ft.colors.BLACK if today.day != start_day else '#0757fa'
                                    ),
                                ],
                                alignment="center",  # Alinear al centro
                                spacing=0,  # Sin espacio entre "Lunes" y el número
                            )
                        ),
                    ]
                ),
                ft.Column(
                    horizontal_alignment="center",
                    controls=[
                        ft.Container(
                            bgcolor=ft.colors.WHITE,  # Fondo para el año
                            padding=5,
                            border_radius=10,
                            content=ft.Text(str(year), size=16, color=ft.colors.BLACK)  # Año
                        ),
                        ft.Row(
                            controls=[
                                ft.Column(
                                    horizontal_alignment="center",
                                    controls=[
                                        ft.Text(
                                            str(days_middle[0]).zfill(2), 
                                            size=20, 
                                            color='#0757fa' if today.day == int(days_middle[0]) else ft.colors.BLACK
                                        )
                                    ]
                                ),
                                ft.Container(width=20),  # Espacio entre Martes y Miércoles
                                ft.Column(
                                    horizontal_alignment="center",
                                    controls=[
                                        ft.Text(
                                            str(days_middle[1]).zfill(2), 
                                            size=20, 
                                            color='#0757fa' if today.day == int(days_middle[1]) else ft.colors.BLACK
                                        )
                                    ]
                                ),
                                ft.Container(width=20),  # Espacio entre Miércoles y Jueves
                                ft.Column(
                                    horizontal_alignment="center",
                                    controls=[
                                        ft.Text(
                                            str(days_middle[2]).zfill(2), 
                                            size=20, 
                                            color='#0757fa' if today.day == int(days_middle[2]) else ft.colors.BLACK
                                        )
                                    ]
                                ),
                            ],
                            alignment="spaceEvenly",
                        ),
                    ],
                ),
                ft.Column(
                    horizontal_alignment="center",
                    controls=[
                        ft.Text(end_month, size=12, color=ft.colors.BLACK),
                        ft.Container(
                            bgcolor=ft.colors.WHITE,  # Fondo del día
                            border_radius=15,
                            padding=10,
                            content=ft.Column(  # Usar Column para alinear "Viernes" y el número
                                controls=[
                                    ft.Text("Viernes", size=12, color=ft.colors.BLACK),  # Viernes
                                    ft.Text(
                                        str(end_day).zfill(2), 
                                        size=20, 
                                        color=ft.colors.BLACK if today.day != end_day else '#0757fa'
                                    ),
                                ],
                                alignment="end",  # Alinear a la derecha
                                spacing=0,  # Sin espacio entre "Viernes" y el número
                            )
                        ),
                    ]
                ),
            ],
        ),
    )
