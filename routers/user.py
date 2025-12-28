from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
from schemas import Blog, ShowBlog, User, ShowUser
from hashing import hash_password
from database import get_db
from repository import user


router = APIRouter(
    prefix="/user",
    tags = ["users"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_user(request:User,db:Session = Depends(get_db)):
    return user.create_user(request,db)

@router.get("/{id}",status_code=200,response_model=ShowUser)
def get_user_by_id(id:int,db:Session=Depends(get_db)):
    return user.get_user_by_id(id,db)

@router.get("/",status_code=200,response_model=List[ShowUser])
def get_all_users(db:Session=Depends(get_db)):
    return user.get_all_users(db)