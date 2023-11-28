from blogging_app import app
from sqlalchemy.orm import Session


from blogging_app import schemas, models, SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

@app.get("/")
async def get():
    return {"Blog App": "Curiosity births Innovations. Discover articles, thoughts, and professionals from authors on any topic"}