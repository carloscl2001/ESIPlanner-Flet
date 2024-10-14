def user_schema(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "name": user["name"],
        "surname": user["surname"],
        "degree": user["degree"],
        "subjects": user.get("subjects", []),  # Usa get para evitar KeyError
    }

def users_schema(users) -> list:
    return [user_schema(user) for user in users]

def subject_schema(subject) -> dict:
    return {
        "name": subject["name"],
        "code": subject["code"],
        "classes": [class_schema(cls) for cls in subject.get("classes", [])],  # Convierte cada clase a dict
    }

def subjects_schema(subjects) -> list:
    return [subject_schema(subject) for subject in subjects]

def class_schema(class_) -> dict:
    return {
        "type": class_["type"],
        "events": [event_schema(event) for event in class_.get("events", [])],  # Convierte cada evento a dict
    }

def classes_schema(classes) -> list:
    return [class_schema(class_) for class_ in classes]

def event_schema(event) -> dict:
    return {
        "date": event["date"],
        "start_hour": event["start_hour"],
        "end_hour": event["end_hour"],
        "location": event["location"],
    }

def events_schema(events) -> list:
    return [event_schema(event) for event in events]