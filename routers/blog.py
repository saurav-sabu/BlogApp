from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from repository import blog

import models
from schemas import Blog, ShowBlog
from database import get_db


router = APIRouter(
    prefix="/blog",
    tags = ["blogs"]
)

@router.get("/")
def get_all_blogs(db:Session = Depends(get_db)):
    return blog.get_all_blogs(db)

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_blog(request:Blog,db:Session = Depends(get_db)):
    return blog.create_blog(request,db)


@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED)
def update_blog(id:int,request:Blog,db:Session = Depends(get_db)):
    return blog.update_blog(id,request,db)


@router.delete("/blog/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id:int,db:Session = Depends(get_db)):
    return blog.delete_blog(id,db)

@router.get("/blog/{id}",status_code=200,response_model=ShowBlog)
def get_blog_by_id(id:int,db:Session = Depends(get_db)):
    return blog.get_blog_by_id(id,db)
