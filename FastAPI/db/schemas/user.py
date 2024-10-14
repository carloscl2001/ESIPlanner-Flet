def user_schema(user) -> dict:
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "username": user["username"],
        "name": user["name"],
        "surname": user["surname"],
        "degree": user["degree"],
        "subjects": user.get("subjects", []),  # Usa get para evitar KeyError
    }

def users_schema(users) -> list:
    return [user_schema(user) for user in users]
