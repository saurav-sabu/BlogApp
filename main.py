from fastapi import FastAPI,Depends,status, Response, HTTPException
from schemas import Blog, ShowBlog, User, ShowUser
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List
import models
from hashing import hash_password


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog",status_code=status.HTTP_201_CREATED,tags=["Blogs"])
def create_blog(request:Blog,db:Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.put("/blog/{id}",status_code=status.HTTP_202_ACCEPTED,tags=["Blogs"])
def update_blog(id:int,request:Blog,db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with {id} not found")
    blog.update(request.dict())
    db.commit()
    return {"status":"done"}


@app.delete("/blog/{id}",status_code=status.HTTP_204_NO_CONTENT,tags=["Blogs"])
def delete_blog(id:int,db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return {"status":"done"}


@app.get("/blog",tags=["Blogs"])
def get_all_blogs(db:Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get("/blog/{id}",status_code=200,response_model=ShowBlog,tags=["Blogs"])
def get_blog_by_id(id:int,db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog {id} not found")
    return blog


@app.post("/user",status_code=status.HTTP_201_CREATED,tags=["Users"])
def create_user(request:User,db:Session = Depends(get_db)):
    new_user = models.User(name=request.name,email=request.email,password=hash_password(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/user/{id}",status_code=200,response_model=ShowUser,tags=["Users"])
def get_user_by_id(id:int,db:Session=Depends(get_db)):
    blog = db.query(models.User).filter(models.User.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog {id} not found")
    return blog

@app.get("/user",status_code=200,response_model=List[ShowUser],tags=["Users"])
def get_all_users(db:Session=Depends(get_db)):
    blog = db.query(models.User).all()
    return blog