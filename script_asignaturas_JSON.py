import json
import os
from datetime import datetime
from icalendar import Calendar, vDatetime
import re

def remove_accents(input_str):
    """
    Elimina los acentos de una cadena dada usando expresiones regulares.
    """
    return re.sub(r'[áàäâã]', 'a',
                  re.sub(r'[éèëê]', 'e',
                         re.sub(r'[íìïî]', 'i',
                                re.sub(r'[óòöôõ]', 'o',
                                       re.sub(r'[úùüû]', 'u',
                                              re.sub(r'[ÁÀÄÂÃ]', 'A',
                                                     re.sub(r'[ÉÈËÊ]', 'E',
                                                            re.sub(r'[ÍÌÏÎ]', 'I',
                                                                   re.sub(r'[ÓÒÖÔÕ]', 'O',
                                                                          re.sub(r'[ÚÙÜÛ]', 'U',input_str))))))))))

def parse_ics_to_json(ics_content):
    """
    Analiza el contenido del archivo ICS y lo convierte a una estructura JSON.
    """
    cal = Calendar.from_ical(ics_content)
    
    courses = {}
    
    def format_datetime(dt):
        """
        Formatea un objeto datetime a una cadena en formato 'YYYY-MM-DD'.
        """
        if isinstance(dt, (datetime, vDatetime)):
            if hasattr(dt, 'tzinfo') and dt.tzinfo is not None:
                dt = dt.astimezone(dt.tzinfo).replace(tzinfo=None)
            return dt.strftime('%Y-%m-%d')
        return str(dt)
    
    def format_time(dt):
        """
        Formatea un objeto datetime a una cadena en formato 'HH:MM'.
        """
        if isinstance(dt, (datetime, vDatetime)):
            if hasattr(dt, 'tzinfo') and dt.tzinfo is not None:
                dt = dt.astimezone(dt.tzinfo).replace(tzinfo=None)
            return dt.strftime('%H:%M')
        return str(dt)
    
    def create_event(date, start_time, end_time, location):
        return {
            "date": date,
            "start_hour": start_time,
            "end_hour": end_time,
            "location": location.strip()
        }

    for component in cal.walk():
        if component.name == "VEVENT":
            location = component.get('location', 'No Location')
            uid = component.get('uid', 'No UID')
            dtstart = component.get('dtstart').dt
            dtend = component.get('dtend').dt
            
            # Obtiene el summary y corta hasta el primer guion
            full_summary = component.get('summary', 'Sin Título')
            summary = remove_accents(full_summary.split('-')[0].strip())

            uid_parts = uid.split('.')
            codigo = uid_parts[0].strip() if len(uid_parts) > 0 else 'Unknown'
            tipo_clase = uid_parts[1].strip() if len(uid_parts) > 1 else 'Unknown'
            
            # Inicializa la entrada de la asignatura si no existe
            if codigo not in courses:
                courses[codigo] = {
                    "code": codigo,
                    "name": summary,
                    "classes": []
                }
            
            # Buscar si ya existe una entrada para este tipo de clase
            class_entry = next((c for c in courses[codigo]["classes"] if c["type"] == tipo_clase), None)
            if class_entry is None:
                class_entry = {
                    "type": tipo_clase,
                    "events": []
                }
                courses[codigo]["classes"].append(class_entry)
            
            initial_event = create_event(
                format_datetime(dtstart),
                format_time(dtstart),
                format_time(dtend),
                location
            )
            
            # Añade el evento inicial solo si no existe
            if initial_event not in class_entry["events"]:
                class_entry["events"].append(initial_event)
            
            rdates = component.get('rdate', [])
            if not isinstance(rdates, list):
                rdates = [rdates]
            
            for rdate in rdates:
                if hasattr(rdate, 'dts'):
                    for date in rdate.dts:
                        recurrent_event = create_event(
                            format_datetime(date.dt),
                            format_time(dtstart),
                            format_time(dtend),
                            location
                        )
                        if recurrent_event not in class_entry["events"]:
                            class_entry["events"].append(recurrent_event)
                elif hasattr(rdate, 'dt'):
                    recurrent_event = create_event(
                        format_datetime(rdate.dt),
                        format_time(dtstart),
                        format_time(dtend),
                        location
                    )
                    if recurrent_event not in class_entry["events"]:
                        class_entry["events"].append(recurrent_event)
    
    return courses

def combine_ics_files(directory):
    """
    Combina todos los archivos ICS en una única estructura JSON.
    """
    all_courses = {}
    
    for file_name in os.listdir(directory):
        if file_name.endswith('.ics'):
            file_path = os.path.join(directory, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    ics_content = f.read()
                courses = parse_ics_to_json(ics_content)
                
                for code, details in courses.items():
                    if code not in all_courses:
                        all_courses[code] = details
                    else:
                        # Combinar las clases y eventos si el código ya existe
                        for class_entry in details["classes"]:
                            existing_class = next((c for c in all_courses[code]["classes"] if c["type"] == class_entry["type"]), None)
                            if existing_class:
                                for event in class_entry["events"]:
                                    if event not in existing_class["events"]:
                                        existing_class["events"].append(event)
                            else:
                                all_courses[code]["classes"].append(class_entry)
            
            except FileNotFoundError:
                print(f"Archivo no encontrado: {file_name}")
            except Exception as e:
                print(f"Error al procesar el archivo {file_name}: {e}")
    
    return all_courses

def save_json_for_each_subject(courses):
    """
    Elimina los archivos JSON existentes y crea un archivo JSON para cada asignatura.
    """
    for file_name in os.listdir('.'):
        if file_name.endswith('.json'):
            os.remove(file_name)
            print(f"Archivo existente eliminado: {file_name}")
    
    for code, details in courses.items():
        output_file = f'{code}.json'
        
        json_output = json.dumps(details, indent=4, ensure_ascii=False)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(json_output)

        
        print(f"Se ha creado el archivo JSON para la asignatura {code} como {output_file}.")

def main():
    directory = '.'  # Usa el directorio actual
    
    combined_courses = combine_ics_files(directory)
    
    save_json_for_each_subject(combined_courses)

if __name__ == "__main__":
    main()