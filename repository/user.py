from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from hashing import hash_password
import models

def create_user(request,db:Session):
    new_user = models.User(name=request.name,email=request.email,password=hash_password(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_id(id:int,db:Session):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user {id} not found")
    return user

def get_all_users(db:Session):
    user = db.query(models.User).all()
    return user