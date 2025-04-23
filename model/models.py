from sqlalchemy import Integer,String,Column,Float,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True)
    email = Column(String,unique=True,index=True)
    hashed_password = Column(String)
    created_at =Column(DateTime, default=datetime.utcnow)

class Flower(Base):
    __tablename__ = "flowers"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,nullable=False)
    price = Column(Float,nullable=False)
    description = Column(String,default="")
    created_at = Column(DateTime,default=datetime.utcnow)
