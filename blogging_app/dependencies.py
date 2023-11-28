from sqlalchemy.orm import Session
from . import models, schemas
from blogging_app.auth import auth_handler
from .database import get_db
from fastapi import Depends


def username_in_DB(username: str, db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.username == username).first()


def email_in_DB(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_signup_details(db: Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        return {
            "user_id": user.user_id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "password": user.password
        }
    
def add_article_to_DB(db: Session, article: schemas.Articles):
    db_article = models.Articles(**article.model_dump())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

def add_user_to_DB(db: Session, user: schemas.User):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def find_article_by_title(db: Session, title: str):
    return db.query(models.Articles).filter(models.Articles.title == title).first()

#############################################
def all_articles_cache(db: Session):
    return db.query(models.Articles).all()

def all_users_cache(db: Session):
    return db.query(models.User).all()

UsersDB_header = " "
article_header = " "
#############################################

def get_articles_by_author(db: Session, author: str):
    return db.query(models.Articles).filter(models.Articles.author == author).all()

def update_user_profile(db: Session, user: schemas.User, update: schemas.UserProfile):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    db_user.first_name = user.first_name
    db_user.last_name = user.last_name
    db_user.bio = update.bio
    db_user.website = update.website
    db_user.twitter = update.twitter
    db_user.facebook = update.facebook
    db_user.instagram = update.instagram
    db.commit()
    db.refresh(db_user)
    # return db_user