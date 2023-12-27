from fastapi import FastAPI, Depends
from blogging_app.routers.home import home_routes
from blogging_app.auth.auth_handler import auth_routes
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker
from .database import SessionLocal
from instance.config import DATABASE_URL


app = FastAPI(
    title="Blog APP",
    description="Curiosity births Innovations. Discover articles, thoughts,\
          and professionals from authors on any topic"
    )

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base: DeclarativeMeta = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.include_router(auth_routes, tags=["auth"], prefix="/auth")
app.include_router(home_routes, tags=["Home Page"], dependencies=[Depends(get_db)])
