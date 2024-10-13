from fastapi import APIRouter, HTTPException
from models import User

router = APIRouter(prefix="/users", 
                    tags=["users"], 
                    responses={404: {"description": "Not found"}})

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


# @router.post("/user/", response_model = User, status_code=201)
# async def create_user(user: User):
#     if type(search_user(user.id)) == User:
#         raise HTTPException(status_code=400, detail="User already exists")
#     else:
#         users.append(user)
#         return user


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