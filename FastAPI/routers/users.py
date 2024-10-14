from fastapi import APIRouter, HTTPException, status
from db.models import User
from db.client import db_client

router = APIRouter(prefix="/users", 
                    tags=["users"], 
                    responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

@router.get("/")
async def get_users():
    return "hola"


# @router.get("/user/{id}")
# async def get_user(id: int):
#     return search_user(id)

# def search_user(id: int):
#     user = filter(lambda user: x.id == id, users)
#     try:
#         return list(users)[0]
#     except:
#         return {"error": "User not found"}

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")

    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.users.find_one({"_id": id}))

    return User(**new_user)

# @router.put("/user/")
# async def update_user(user: User):
#     if type(search_user(user.id)) == User:
#         users.remove(user)
#         users.append(user)
#         return user
#     else:
#         return {"error": "User not found"}

# @router.delete("/user/{id}")
# async def delete_user(id: int):
#     user = search_user(id)
#     if type(user) == User:
#         users.remove(user)
#         return user
#     else:
#         return {"error": "User not found"}

# @router.delete("/user/")
# async def delete_all_users():
#     users.clear()
#     return {"message": "All users deleted"}