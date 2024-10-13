from pydantic import BaseModel
from typing import List

# Modelo para cada tipo de clase dentro de una asignatura
class ClassType(BaseModel):
    class_name: str
    teacher: str
    schedule: str

# Modelo para las asignaturas
class Subject(BaseModel):
    subject_name: str
    subject_code: str
    class_types: List[ClassType]

# Modelo para el usuario
class User(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    degree: str
    subjects: List[Subject] | None# Aquí usamos una lista de asignaturas
    password: str