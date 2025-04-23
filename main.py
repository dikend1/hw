from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import schemas,auth
from repo import UsersRepo, FlowersRepo
from model import models
app = FastAPI()


@app.post("/signup",response_model=schemas.UserOut)
def signup(user_in: schemas.UserCreate, db:Session = Depends(get_db)):
    repository = UsersRepo.UserRepository(db)
    user = repository.get_by_email(user_in.email)
    if user:
        raise HTTPException(status_code=400,detail="Email уже занят")
    return repository.create(user_in)

@app.post("/login",response_model=schemas.Token)
def login(form:schemas.LoginForm, db:Session = Depends(get_db)):
    repo = UsersRepo.UserRepository(db)
    user = repo.get_by_email(form.email)
    if not user or not auth.verify_password(form.password,user.hashed_password):
        raise HTTPException(401,detail="Неверные учётные данные")
    return auth.create_access_token_for_user(user)

@app.get("/profile",response_model=schemas.UserOut)
def profile(current_user:models.User = Depends(auth.get_current_user)):
    return current_user

@app.get("/flowers",response_model=list[schemas.FlowerOut])
def list_flowers(db:Session = Depends(get_db)):
    return FlowersRepo.FlowersRepository(db).list_all()

@app.post("/flowers",response_model=schemas.FlowerOut)
def create_flower(flower_in: schemas.FlowerCreate, db: Session = Depends(get_db)):
    return FlowersRepo.FlowersRepository(db).create(flower_in)

@app.patch("/flowers/{flower_id}",response_model=schemas.FlowerOut)
def update_flower(flower_id: int,flower_upd:schemas.FlowerUpdate, db: Session = Depends(get_db)):
    repo = FlowersRepo.FlowersRepository(db)
    flower = repo.get(flower_id) or HTTPException(status_code=404,detail="Не найдено")
    return repo.update(flower,flower_upd.dict(exclude_unset=True))

@app.delete("/flowers/{flower_id}",status_code=204)
def delete_flower(flower_id: int,db:Session = Depends(get_db)):
    repo = FlowersRepo.FlowersRepository(db)
    flower = repo.get(flower_id) or HTTPException(status_code=404,detail="Не найдено")
    repo.delete(flower)



