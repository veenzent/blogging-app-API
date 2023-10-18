from fastapi import APIRouter
from uuid import UUID


home_routes = APIRouter


@home_routes.get("/")
async def home():
    return {"message": "Welcome to Blogging Made Easier"}