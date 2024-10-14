from pydantic import BaseModel, Field
from typing import Optional, List


# Modelo para los eventos
class Event(BaseModel):
    date: str
    star_hour: str
    end_hour: str
    location: str

#Modelo para los tipos de clases
class Class(BaseModel):
    type: str
    events: List[Event]

# Modelo para la asignatura
class Subject(BaseModel):
    name: str
    code: str
    classes: List[Class]

# Modelo para el usuario
class User(BaseModel):
    id : str | None = Field(default = None)
    username: str
    email: str
    name: str
    surname: str
    degree: str
    subjects: Optional[List[str]] = None


