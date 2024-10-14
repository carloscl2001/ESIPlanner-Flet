# Clase en vídeo: https://youtu.be/_y9qQZXE24A?t=20480

### Users DB API ###

from fastapi import APIRouter, HTTPException, status
from db.models.user import User, Subject, Class, Event
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(prefix="/users",
                   tags=["users"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

@router.get("/", response_model=list[User])
async def users():
    try:
        users_list = list(db_client.users.find())  # Convierte el cursor en una lista
        print(f"Users encontrados: {users_list}")  # Agrega logs para ver los datos
        return users_schema(users_list)  # Aplica el schema a la lista
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")



@router.get("/{id}")  # Path
async def user(id: str):
    return search_user("_id", ObjectId(id))


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")

    # Creamos un diccionario con los datos del usuario
    user_dict = dict(user)

    # Eliminamos el campo id que no le pasamos al post para que no enviemos un None
    del user_dict["id"]

    # Solo eliminamos el campo subjects si no está presente o está vacío
    if "subjects" in user_dict and not user_dict["subjects"]:
        del user_dict["subjects"]

    # Insertamos el nuevo usuario en la base de datos
    id = db_client.users.insert_one(user_dict).inserted_id

    # Recuperamos el usuario recién creado
    new_user = user_schema(db_client.users.find_one({"_id": id}))

    return User(**new_user)

@router.put("/", response_model=User)
async def user(user: User):

    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_client.users.find_one_and_replace(
            {"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"error": "No se ha actualizado el usuario"}

    return search_user("_id", ObjectId(user.id))


@router.delete("/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def user(username: str):

    found = db_client.users.find_one_and_delete({"username": username})

    if not found:
        return {"error": "No se ha eliminado el usuario"}

# Helper


def search_user(field: str, key):

    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"error": "No se ha encontrado el usuario"}