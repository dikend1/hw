from sqlalchemy.orm import Session
from model import models 
from passlib.context import CryptContext
import schemas

class FlowersRepository:
    def __init__(self,db: Session):
        self.db = db
    
    def list_all(self):
        return self.db.query(models.Flower).all()
    
    def create(self,flower_in:schemas.FlowerCreate):
        flower = models.Flower(**flower_in.dict())
        self.db.add(flower)
        self.db.commit()
        self.db.refresh(flower)
        return flower
    

    def get(self,flower_id: int):
        return self.db.query(models.Flower).get(flower_id)
    
    def update(self,flower: models.Flower,updates: dict):
        for k, v in updates.items():
            setattr(flower,k,v)
        self.db.commit()
        self.db.refresh(flower)
        return flower
    
    def delete(self,flower: models.Flower):
        self.db.delete(flower)
        self.db.commit()
