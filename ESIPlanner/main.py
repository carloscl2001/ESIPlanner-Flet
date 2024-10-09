import flet as ft
from weekly_date_range import WeeklyDateRange
from datetime import datetime, timedelta

# Función para calcular las semanas
def get_weeks_from_today(limit=10):
    today = datetime.today()

    # Encuentra el lunes de esta semana
    if today.weekday() == 0:  # Si hoy es lunes
        monday = today
    else:
        monday = today - timedelta(days=today.weekday())  # El lunes de esta semana

    weeks = []
    for i in range(limit):
        start_day = monday + timedelta(weeks=i)  # Lunes de cada semana
        end_day = start_day + timedelta(days=4)  # El viernes de esa semana
        days_middle = [
            str(start_day.day + 1).zfill(2),  # Martes
            str(start_day.day + 2).zfill(2),  # Miércoles
            str(start_day.day + 3).zfill(2),  # Jueves
        ]
        weeks.append({
            "start_day": start_day,
            "end_day": end_day,
            "days_middle": days_middle,
        })
    return weeks

def main(page: ft.Page):
    page.title = "Weekly Date Range Scroll Example"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    
    # Crear el ListView con scroll, sin auto-scroll
    weeks_list = ft.ListView(expand=True, spacing=10, padding=20, auto_scroll=False)

    # Espaciado en la parte superior para evitar superposición
    header_space = ft.Container(height=20)  # Ajusta la altura según sea necesario

    # Generar las semanas y añadirlas al ListView
    weeks = get_weeks_from_today(limit=10)
    for week in weeks:
        weeks_list.controls.append(
            WeeklyDateRange(
                start_day=str(week["start_day"].day).zfill(2),
                start_month=week["start_day"].strftime("%B"),
                end_day=str(week["end_day"].day).zfill(2),
                end_month=week["end_day"].strftime("%B"),
                year=week["start_day"].year,
                days_middle=week["days_middle"]
            )
        )
    
    # Añadir el espaciado y el ListView a la página
    page.add(header_space, weeks_list)

ft.app(target=main)
