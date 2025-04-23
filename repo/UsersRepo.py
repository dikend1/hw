from sqlalchemy.orm import Session
from model import models 
from passlib.context import CryptContext
import schemas


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository:
    def __init__(self,db: Session):
        self.db = db
    

    def create(self,user_in: schemas.UserCreate)->models.User:
        hashed = pwd_context.hash(user_in.password)
        user = models.User(email = user_in.email, hashed_password=hashed)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_by_email(self,email:str)->models.User | None:
        return self.db.query(models.User).filter(models.User.email == email).first()
    
    def get(self,user_id: int)->models.User | None:
        return self.db.query(models.User).get(user_id)

