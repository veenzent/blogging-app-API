from blogging_app import app
from sqlalchemy.orm import Session
from blogging_app.models import Base
from blogging_app import models, SessionLocal, engine


models.Base.metadata.create_all(bind=engine)
existing_tables = Base.metadata.tables.keys()
print("Existing tables:", existing_tables)


@app.get("/")
async def get():
    return {"Blog App": "Curiosity births Innovations. Discover articles, thoughts, and professionals from authors on any topic"}



if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run("main:app", reload=True)