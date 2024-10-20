from pydantic import BaseModel, Field
from typing import Optional, List

# Modelo para representar las asignaturas del usuario con tipos de clase
class UserSubject(BaseModel):
    code: str  # Código de la asignatura
    types: List[str]  # Lista de tipos de clases, por ejemplo, ["A1", "B1", "C1"]

# Modelo para el usuario que usa el esquema UserSubject en lugar de modificar Subject
class User(BaseModel):
    id: str | None = Field(default=None)
    email: str
    username: str
    password: str
    name: str
    surname: str
    degree: str
    subjects: Optional[List[UserSubject]] = None  # Lista de asignaturas con tipos de clase