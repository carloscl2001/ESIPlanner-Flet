from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

#CONSTANTS
ALGORITHM = "HS256"
ACCES_TOKEN_DURATION = 1
SECRET = "201d573bd7d1344d3a3bfce1550b69102fd11be3db6d379508b6cccc58ea230b"


oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = form.username 
    #comprobar que exista el usuario
    
    #comprobar que la contraseña sea correcta
    if not crypt.verify(form.password, user_db.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    #generar token
    access_token_expires = timedelta(minutes=ACCES_TOKEN_DURATION)
    expire = datetime.utcnow() + access_token_expires
    access_token = {
        "sub": user_db.username,
        "exp": expire
    }

    return {"access_token": jwt.encode(access_token, SECRET, algorithm = ALGORITHM), "token_type": "bearer"}

@router.get("/users/me")
async def read_users_me(user: User = Depends()):



async def current_user(token: str = Depends(oauth2)):
    user = 
    if not user:
        raise HTTPException(
                status_code= status.HTTP_401_BAD_REQUEST, 
                detail="Unauthorized",
                headfers={"WWW-Authenticate": "Bearer"})
    return user

