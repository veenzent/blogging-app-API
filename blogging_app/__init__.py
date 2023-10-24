from fastapi import FastAPI, HTTPException
from blogging_app.routers.home import home_routes

app = FastAPI(title="Blog APP", description="Curiosity births Innovations. Discover articles, thoughts, and professionals from authors on any topic")


app.include_router(home_routes, tags=["Home Page"])

