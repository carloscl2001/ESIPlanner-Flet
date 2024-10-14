from pydantic import BaseModel, Field
from typing import Optional, List


# Modelo para el usuario
class User(BaseModel):
    id : str | None = Field(default = None)
    email: str
    username: str
    name: str
    surname: str
    degree: str
    subjects: Optional[List[str]] = None


