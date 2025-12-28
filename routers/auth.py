from fastapi import APIRouter, Depends, HTTPException, status
from schemas import Login
from sqlalchemy.orm import Session
from database import get_db
from hashing import verify_password
import models
from datetime import timedelta
from security import create_access_token, ACCESS_TOKEN_EXPIRE_IN_MINUTES


router = APIRouter(
    tags=["auth"]
)

@router.post("/login")
def login(request:Login,db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Invalid credentials")
    if not verify_password(request.password,user.password):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Incorrect Password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_IN_MINUTES)
    access_token = create_access_token(
        data={"sub":user.email}
    )
    return {"access_token":access_token,"token_type":"bearer"}