from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(prefix="/users",
                   tags=["users"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

@router.get("/", response_model=list[User])
async def users():
    try:
        users_list = list(db_client.users.find())  # Convierte el cursor en una lista
        print(f"Users encontrados: {users_list}")  # Agrega logs para ver los datos
        return users_schema(users_list)  # Aplica el schema a la lista
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")



@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="users already exists")

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