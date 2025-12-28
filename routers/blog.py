from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import models
from schemas import Blog, ShowBlog
from database import get_db


router = APIRouter(
    prefix="/blog",
    tags = ["blogs"]
)

@router.get("/")
def get_all_blogs(db:Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_blog(request:Blog,db:Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED)
def update_blog(id:int,request:Blog,db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with {id} not found")
    blog.update(request.dict())
    db.commit()
    return {"status":"done"}


@router.delete("/blog/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id:int,db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return {"status":"done"}

@router.get("/blog/{id}",status_code=200,response_model=ShowBlog)
def get_blog_by_id(id:int,db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog {id} not found")
    return blog
