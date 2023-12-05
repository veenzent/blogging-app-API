from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base


# User Sign-in
class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(100), unique=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(255), unique=True)
    password = Column(String(255))
    bio = Column(String(500))
    website = Column(String(100))
    twitter = Column(String(100))
    facebook = Column(String(100))
    instagram = Column(String(100))
    last_updated_at = Column(DateTime(), index=True, default=datetime.utcnow)
    
    posts = relationship("Articles", back_populates="user")
    posts_count = Column(Integer, default=0)
    

class Articles(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String(255), index=True)
    author = Column(String(255))
    author_username = Column(String(255), ForeignKey('user.username'), nullable=False)
    content = Column(Text, index=True, nullable=False)
    date_published  =Column(DateTime(), index=True, default=datetime.utcnow)
    last_updated = Column(DateTime(), index=True, default=datetime.utcnow)

    user = relationship("User", back_populates="posts")
