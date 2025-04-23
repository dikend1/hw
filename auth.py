from datetime import datetime, timedelta
from jose import JWTError,jwt
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from model import models
import schemas
from database import get_db
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
def verify_password(plain:str,hashed:str)->bool:
    return pwd_context.verify(plain,hashed)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = "DIKO"
ALGALGORITHM   = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token_for_user(user:models.User)->schemas.Token:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub":user.email,"id":user.id,"exp":expire}
    token = jwt.encode(payload,SECRET_KEY,algorithm=ALGALGORITHM)
    return {"access_token":token,"token_type":"bearer"}

def get_current_user(db:Session = Depends(get_db),
                     token: str = Depends(oauth2_scheme))->models.User:
    credentials_exc = HTTPException(status_code=401,detail="Неверные учётные данные",headers={"WWW-Authenticate": "Bearer"})
    try:
        data = jwt.decode(token,SECRET_KEY,algorithms=[ALGALGORITHM])
        user_id = data.get("id")
        if user_id is None:
            raise credentials_exc
    except JWTError:
        raise credentials_exc
    
    user = db.query(models.User).get(user_id)
    if user is None:
        raise credentials_exc
    return user