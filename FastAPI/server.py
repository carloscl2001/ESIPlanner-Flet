
# Inicia el server: uvicorn main:app --reload
# Detener el server: CTRL+C

# Documentación con Swagger: http://127.0.0.1:8000/docs
# Documentación con Redocly: http://127.0.0.1:8000/redoc

from fastapi import FastAPI
from routers import users
from routers import subjects
from routers import auth

# Instanciamos la aplicación
app = FastAPI()

# Incluimos los routers
app.include_router(users.router)
app.include_router(subjects.router)
app.include_router(auth.router)


# Definimos una peticion básica
@app.get("/")
async def root():
    return "Hola FastAPI!"
