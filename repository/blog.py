from sqlalchemy.orm import Session
from fastapi import HTTPException,status
import models

def get_all_blogs(db:Session):
    blogs = db.query(models.Blog).all()
    return blogs

def create_blog(request,db:Session):
    new_blog = models.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def delete_blog(id:int,db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return {"status":"done"}

def update_blog(id:int,request,db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with {id} not found")
    blog.update(request.dict())
    db.commit()
    return {"status":"done"}

def get_blog_by_id(id:int,db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog {id} not found")
    return blog