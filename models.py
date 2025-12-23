from sqlalchemy import Column, String, Integer
from pydantic import BaseModel
from database import Base

class Blog(Base):

    __tablename__ = "blogs"
    
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    body = Column(String)
