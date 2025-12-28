from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
from schemas import Blog, ShowBlog, User, ShowUser
from hashing import hash_password
from database import get_db

router = APIRouter(
    prefix="/user",
    tags = ["users"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_user(request:User,db:Session = Depends(get_db)):
    new_user = models.User(name=request.name,email=request.email,password=hash_password(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",status_code=200,response_model=ShowUser)
def get_user_by_id(id:int,db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user {id} not found")
    return user

@router.get("/",status_code=200,response_model=List[ShowUser])
def get_all_users(db:Session=Depends(get_db)):
    user = db.query(models.User).all()
    return user