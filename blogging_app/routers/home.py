from fastapi import APIRouter, Form, HTTPException
from typing import Annotated
from uuid import UUID
from blogging_app.models import User, UserProfile, Articles, UpdateArticle, UpdateArticleResponse
import csv
import datetime
from blogging_app.reusables import get_total_users, add_article_to_DB, username_in_DB, all_articles_cache, username_in_DB, add_user_to_DB


home_routes = APIRouter()


@home_routes.get("/index")
async def home():
    return {"message": "Curiosity births Innovations. Discover articles, thoughts, and professionals from authors on any topic"}

@home_routes.get("/about")
async def about():
    return {"message": "About Page coming soon!"}

@home_routes.get("/contacts")
async def contacts():
    return {"message": "Contacts Page coming soon!"}


# - - - - - T R E N D I N G - A R T I C L E S - - - - -
@home_routes.get("/get-blogs")
async def get_blogs():
    with open("blogging_app/all_articles.csv", "r") as all_articles:
        reader = csv.reader(all_articles)
        next(reader)
        trending = []
        for i, article in enumerate(reader):
            if i <= 4:
                article = Articles(title=article[0], author=article[1], content=article[2], date_published=article[3])
                trending.append(article)
    return{"Trending Articles": trending}


# - - - - - W R I T E - A R T I C L E - - - - -
@home_routes.post("/create-blog", response_model=Articles)
async def create_blog(
    username: Annotated[str, Form(max_length=100)],
    title: Annotated[str, Form()],
    content: Annotated[str, Form(...)]
):
    # get author
    author = ""
    with open("blogging_app/UsersDB.csv", "r") as UsersDB:
        reader = csv.reader(UsersDB)
        next(reader)
        for user in reader:
            if username == user[1]:
                author = f"{user[2]} {user[3]}"
                article = Articles(title=title, author=author, content=content, date_published=str(datetime.datetime.now()))
                add_article_to_DB(article)
                return article
    raise HTTPException(status_code=404, detail="User not found, Sign up to write an article!")


# - - - - - E D I T - A R T I C L E - - - - -
@home_routes.put("/dashboaard/{username}/{title}/edit-blog", response_model=UpdateArticleResponse)
async def edit_blog(username: str, title: str, updated_article: UpdateArticle):
    user = username_in_DB(username)
    if user:
        caches = all_articles_cache()

        with open("blogging_app/all_articles.csv", "w", newline="") as all_articles:
            writer = csv.writer(all_articles)
            for i, article in enumerate(caches):
                if title == article[0]:
                    update = [updated_article.title, caches[i][1], updated_article.content, caches[i][3]]
                    writer.writerow(update)
                else:
                    writer.writerow(article)
        return UpdateArticleResponse(title=updated_article.title, author=update[1], content=updated_article.content, date_published=update[3], last_updated=datetime.datetime.now())
    raise HTTPException(status_code=404, detail="Title not found!")


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
    if username_in_DB(username):
        raise HTTPException(status_code=400, detail="Username already exists!")
    if confirm_password == password:
        total_users = get_total_users()
        id = str(UUID(int=total_users + 1))
        new_user = User(id=id, username=username, first_name=first_name, last_name=last_name, email=email, password=password)

        # new user details
        row = [new_user.id, new_user.username, new_user.first_name, new_user.last_name, new_user.email, new_user.password]

        # add new user to database
        add_user_to_DB(new_user)
    return {"message": "Sign-up successful!"}


# - - - - - L O G I N / S I G N - I N- - - - - -
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
        raise HTTPException(status_code=401, detail="Username and/or password incorrect")


# - - - - - U P D A T E - P R O F I L E - - - - -
@home_routes.put("/dashboard/{username}/update-profile", response_model=UserProfile)
async def update_profile(username: str, profile: UserProfile):

    return {"message": "Profile updated successfully!"}
