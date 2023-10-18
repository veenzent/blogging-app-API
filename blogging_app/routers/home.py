from fastapi import APIRouter, Form, HTTPException
from blogging_app.models import SignIn, User


home_routes = APIRouter()


@home_routes.get("/")
async def home():
    return {"message": "Curiosity births Innovations. Discover articles, thoughts, and professionals from authors on any topic"}

@home_routes.get("/about")
async def about():
    return {"message": "About Page coming soon!"}

@home_routes.get("/contacts")
async def contacts():
    return {"message": "Contacts Page coming soon!"}

# - - - - - S I G N - U P - - - - -
@home_routes.post("/sign-up")
async def sign_up(form: User = Form(...)):
    return {"message": "Sign-up successful!"}

@home_routes.post("/sign-in")
async def sign_in(credentials: SignIn):
    if credentials.email != "email" or credentials.password != "password":
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    return {"message": "Sign in successful!"}