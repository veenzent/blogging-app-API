from fastapi import APIRouter, Form, HTTPException
from typing import Annotated
from uuid import UUID
from blogging_app.models import User
import csv


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
async def sign_up(
  username: Annotated[str, Form(max_length=100)],
  first_name: Annotated[str, Form(max_length=100)],
  last_name: Annotated[str, Form(max_length=100)],
  email: Annotated[str, Form(max_length=100)],
  password: Annotated[str, Form(max_length=100)],
  confirm_password: Annotated[str, Form(max_length=100)]
):
    if confirm_password == password:
        new_user: User

        # get total users currently in the database
        with open("./blogging_app/UsersDB.csv", "r") as UsersDB:
            reader = csv.reader(UsersDB)
            total_users = len(list(reader))
        id = str(UUID(int=total_users + 1))

        # new user details
        row = [
            {"id": id, new_user.username: username, new_user.first_name: first_name, new_user.last_name: last_name, new_user.email: email, new_user.password: password}
        ]

        # add new user to database
        with open("./blogging_app/UsersDB.csv", "a", newline="") as UsersDB:
            writer = csv.DictWriter(UsersDB, fieldnames=["username", "firstname", "lastname", "email", "password", "confirm_password"])
            writer.writeheader()
            writer.writerow(row[0])
    return {"message": "Sign-up successful!", "data": row}

@home_routes.post("/sign-in")
async def sign_in(
  username: Annotated[str, Form(max_length=100)],
  password: Annotated[str, Form(max_length=100)]
):
    # if credentials.email != "email" or credentials.password != "password":
        # raise HTTPException(status_code=401, detail="Invalid Credentials")
    return {"message": "Sign in successful!"}