from fastapi import APIRouter, Form, HTTPException
from typing import Annotated
from uuid import UUID
from blogging_app.models import User, UserProfile, all_articles, Articles
import csv
import datetime
from blogging_app.reusables import get_total_users


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

# list of blogs published by various users
@home_routes.get("/trending_articles")
async def trending_articles():
    if all_articles:
        trending = [i for i, article in enumerate(all_articles) if i < 6]
        return {"Trending Articles": trending}
    return{"Trending Articles": []}

# - - - - - W R I T E - A R T I C L E - - - - -
@home_routes.post("/write", response_model=Articles)
async def write_article(
    username: Annotated[str, Form(max_length=100)],
    title: Annotated[str, Form()],
    content: Annotated[str, Form(...)]
):
    author = ""
    with open("blogging_app/UsersDB.csv", "r") as UsersDB:
        reader = csv.reader(UsersDB)
        next(reader)
        for user in reader:
            if username == user[1]:
                author = f"{user[2]} {user[3]}"
                article = Articles(title=title, author=author, content=content, date_pblished=datetime.datetime.now())
            return article
    return {"message": "User not found, Sign up to write an article!"}

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
        total_users = get_total_users()
        id = str(UUID(int=total_users + 1))
        new_user= User(id=id, username=username, first_name=first_name, last_name=last_name, email=email, password=password)

        # new user details
        row = [new_user.id, new_user.username, new_user.first_name, new_user.last_name, new_user.email, new_user.password]

        # add new user to database
        with open("./blogging_app/UsersDB.csv", "a", newline="") as UsersDB:
            writer = csv.writer(UsersDB)
            writer.writerow(row)
    return {"message": "Sign-up successful!"}

@home_routes.post("/sign-in")
async def sign_in(
  username: Annotated[str, Form(max_length=100)],
  password: Annotated[str, Form(max_length=100)]
):
    with open("blogging_app/UsersDB.csv", "r") as UsersDB:
        reader = csv.reader(UsersDB)
        next(reader)
        for user in reader:
            if username == user[1] and password == user[-1]:
                return {"message": f"Welcome back {user[2]}!"}
        return HTTPException(status_code=401, detail="Username and/or password incorrect")

@home_routes.put("/update-profile/{username}")
async def update_profile(username: str, profile: UserProfile):
    return {"message": "Profile updated successfully!"}
