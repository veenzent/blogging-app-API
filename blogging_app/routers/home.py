from fastapi import APIRouter, Form, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated, Optional
import uuid
from blogging_app import models
import csv
from datetime import datetime, timedelta
from blogging_app.auth import auth_handler
from blogging_app.reusables import add_article_to_DB, username_in_DB, all_articles_cache, all_users_cache, username_in_DB, add_user_to_DB, get_user_signup_details, get_articles_by_author, UsersDB_header, article_header, find_article_by_title, update_user_profile, email_in_DB, authenticate_user


home_routes = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/sign-in")


@home_routes.get("/index")
async def home():
    """
    GET request to "/index" endpoint.

    Response:
        dict: A dictionary containing a message about the contents available on the website.
    """
    return {"message": "Curiosity births Innovations. Discover articles, thoughts, and professionals from authors on any topic"}

@home_routes.get("/about")
async def about():
    """
    Retrieves information about the about page.

    :return: A dictionary containing the message "About Us!"
    """
    return {"message": "About Us!"}

@home_routes.get("/contacts")
async def contacts():
    """
    Gets the contacts page information.

    Response:
        dict: A dictionary containing the message "Contacts Us!".
    """
    return {"message": "Contacts Us!"}


# - - - - - T R E N D I N G - A R T I C L E S - - - - -
@home_routes.get("/get-blogs")
async def get_latest_blogs():
    """
    Retrieves the latest blogs from the all_articles.csv file.

    Returns:
    dict: A dictionary containing the latest blogs, where the keys are the blog titles and the values are the corresponding blog articles.
    """
    with open("blogging_app/all_articles.csv", "r") as all_articles:
        reader = csv.reader(all_articles)
        next(reader)
        reader = sorted(reader, key=lambda x: x[3], reverse=True)
        trending = []
        for i, article in enumerate(reader):
            if i <= 4:
                article = models.Articles(title=article[0], author=article[1], content=article[2], date_published=article[3])
                trending.append(article)
    return{"Latest Blogs": trending}


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
    """
    Handle the sign-up request.

    Parameters:
        - username (str): The username of the new user.
        - first_name (str): The first name of the new user.
        - last_name (str): The last name of the new user.
        - email (str): The email of the new user.
        - password (str): The password of the new user.
        - confirm_password (str): The confirmation password for the new user.
    
    Returns:
        dict: A dictionary containing the success message if the sign-up is successful.
    
    Raises:
        HTTPException: If the username already exists in the database.
    """
    if username_in_DB(username):
        raise HTTPException(status_code=400, detail="Username already exists!")
    if email_in_DB(email):
        raise HTTPException(status_code=400, detail="Email already exists!")
    if confirm_password != password:
        raise HTTPException(status_code=400, detail="Passwords do not match!")
    else:
        id = str(uuid.uuid4())
        new_user = models.User(id=id, username=username, first_name=first_name, last_name=last_name, email=email, password=auth_handler.get_password_hash(password))

        # new user details
        row = [new_user.id, new_user.username, new_user.first_name, new_user.last_name, new_user.email, new_user.password, 'Write something about yourself', " ", " ", " ", " ", " ", [], " "]
        # print(row)

        # add new user to database
        add_user_to_DB(row)
    return {"message": "Sign-up successful!."}


# - - - - - L O G I N / S I G N - I N- - - - - -
@home_routes.post("/sign-in", response_model=models.Token)
async def sign_in(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Signs in a user with their provided username and password.

    Parameters:
    - username (str): The username of the user.
    - password (str): The password of the user.

    Returns:
    - dict: A dictionary with a message if the sign-in was successful, otherwise raise an HTTPException.

    Raises:
    - HTTPException: If the provided username and/or password is incorrect.
    """
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})

    user =  authenticate_user(form_data.username, form_data.password)
    if user:
        access_token_expires = timedelta(minutes=auth_handler.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth_handler.create_access_token(data={"sub": user[1]}, expires_delta=access_token_expires)
    else:
        raise credential_exception
    return {"access_token": access_token, "token_type": "bearer"}


# - - - - - U P D A T E - P R O F I L E - - - - -
@home_routes.put("/dashboard/{username}/update-profile", response_model=models.UserProfile)
async def update_profile(
    username: Annotated[str, Depends(auth_handler.authorize_url)],
    bio: Optional[Annotated[str | None, Form(default="Write something about yourself!")]],
    website: Optional[Annotated[str, Form()]],
    twitter: Optional[Annotated[str, Form()]],
    facebook: Optional[Annotated[str, Form()]],
    instagram: Optional[Annotated[str, Form()]]
):
    """
    Update the profile of a user.

    Args:
        username (str): The username of the user.
        bio (Optional[str]): The user's biography. Defaults to "Write something about yourself!".
        website (Optional[str]): The user's website.
        twitter (Optional[str]): The user's Twitter handle.
        facebook (Optional[str]): The user's Facebook profile.
        instagram (Optional[str]): The user's Instagram handle.

    Returns:
        UserProfile: The updated user profile.

    Raises:
        HTTPException: If the user is not found.
    """
    if username_in_DB(username):
        signup_data = get_user_signup_details(username)
        author = f"{signup_data[2]} {signup_data[3]}"
        articles = get_articles_by_author(author)
        profile_update = models.UserProfile(
            id=signup_data[0],
            username=signup_data[1],
            first_name=signup_data[2],
            last_name=signup_data[3],
            email=signup_data[4],
            password=signup_data[5],            
            bio=bio,
            website=website,
            twitter=twitter,
            facebook=facebook,
            instagram=instagram,
            last_updated_at=str(datetime.today().strftime("%d-%B-%Y %H:%M:%S")),
            posts=[article for article in articles],
            posts_count=len(articles)
        )

        update = [
            profile_update.id, profile_update.username, profile_update.first_name, profile_update.last_name, profile_update.email, profile_update.password, profile_update.bio, profile_update.website, profile_update.twitter, profile_update.facebook, profile_update.instagram, profile_update.last_updated_at, profile_update.posts, profile_update.posts_count
        ]
        update[12] = articles
        update_user_profile(signup_data, update)
        return profile_update
    raise HTTPException(status_code=404, detail="User not found!")


# - - - - - M Y - P R O F I L E - - - - -
@home_routes.get("/dashboard/profile", response_model=models.UserProfileResponse)
async def my_profile(username: Annotated[str, Depends(auth_handler.authorize_url)]):
    users = all_users_cache()
    for user in users:
        if username == user[1]:
            author = f"{user[2]} {user[3]}"
            articles = get_articles_by_author(author)
            profile = models.UserProfileResponse(
                id=user[0], username=user[1], first_name=user[2], last_name=user[3], email=user[4], password=user[5], bio=user[6], website=user[7], twitter=user[8], facebook=user[9], instagram=user[10], last_updated_at=user[11], posts=[models.Articles(**article) for article in articles], posts_count= len(articles)
            )
            return profile


# - - - - - C R E A T E - B L O G - - - - -
@home_routes.post("/create-blog", response_model=models.Articles)
async def create_blog(
    username: Annotated[str, Depends(auth_handler.authorize_url)],
    title: Annotated[str, Form()],
    content: Annotated[str, Form(...)]
):
    """
    Creates a new blog post.

    Parameters:
        username (str): The username of the author. Max length: 100 characters.
        title (str): The title of the blog post.
        content (str): The content of the blog post.

    Returns:
        BlogPost: The newly created blog post.

    Raises:
        HTTPException: If the user is not found in the database.
    """
    # get author
    author = ""
    print(username)
    with open("blogging_app/UsersDB.csv", "r") as UsersDB:
        reader = csv.reader(UsersDB)
        next(reader)
        for user in reader:
            if username == user[1]:
                author = f"{user[2]} {user[3]}"
                article = models.Articles(title=title, author=author, content=content, date_published=str(datetime.today().strftime("%d-%B-%Y %H:%M:%S")))
                add_article_to_DB(article)
                return article
    raise HTTPException(status_code=404, detail="User not found, Sign up to start writing blogs!")


# - - - - - E D I T - A R T I C L E - - - - -
@home_routes.put("/dashboaard/{username}/edit-blog", response_model=models.UpdateArticleResponse)
async def edit_blog(username: Annotated[str, Depends(auth_handler.authorize_url)], title: str, updated_article: models.UpdateArticle):
    """
    Edit a blog article by title.

    Parameters:
    - `username` (str): The username of the author of the article.
    - `title` (str): The title of the article to be edited.
    - `updated_article` (UpdateArticle): The updated article object.

    Returns:
    - `UpdateArticleResponse`: The response object containing the updated article details.

    Raises:
    - `HTTPException`: If the specified title is not found.

    Description:
    This function edits a blog article by updating the specified article's title,
    content, and date published. It first checks if the specified username exists
    in the database. If found, it retrieves all articles from the cache and writes
    them to the articlesDB(csv) file. The function then iterates through the
    articles and updates the specified article with the new title, content, and
    date published. Finally, it returns the updated article details in the
    `UpdateArticleResponse` object. If the specified title is not found, it raises
    an HTTPException with a status code of 404.

    Note:
    - The function assumes that the article cache is stored in memory as `caches`.
    - The article details are written to the "all_articles.csv" file.
    - The `UpdateArticle` object contains the updated article's title, content,
      and date published.
    """
    user = username_in_DB(username)
    if user:
        caches = all_articles_cache()

        with open("blogging_app/all_articles.csv", "w", newline="") as all_articles:
            writer = csv.writer(all_articles)
            writer.writerow(article_header)
            for i, article in enumerate(caches):
                if title == article[0]:
                    update = [updated_article.title, caches[i][1], updated_article.content, caches[i][3]]
                    writer.writerow(update)
                else:
                    writer.writerow(article)
        return models.UpdateArticleResponse(title=updated_article.title, author=update[1], content=updated_article.content, date_published=update[3], last_updated=datetime.today().strftime("%d-%B-%Y %H:%M:%S"))
    raise HTTPException(status_code=404, detail="Title not found!")


# - - - - - M Y - B L O G S - - - - -
@home_routes.get("/dashboaard/{username}/my-blogs")
async def my_blogs(username: Annotated[str, Depends(auth_handler.authorize_url)]):
    """
    Retrieves the blogs created by the specified user.

    Parameters:
        username (str): The username of the user whose blogs are being retrieved.

    Returns:
        dict: A dictionary containing the user's blogs, if any exist.

    Raises:
        HTTPException: If the specified user does not exist or has no blogs.
            - status_code: The HTTP status code indicating the error.
            - detail: A description of the error.
    """
    if username_in_DB(username):
        with open("blogging_app/UsersDB.csv", "r") as UsersDB:
            reader = csv.reader(UsersDB)
            next(reader)
            for user in reader:
                if username == user[1]:
                    author = f"{user[2]} {user[3]}"
        articles = get_articles_by_author(author)
        if articles:
            return {"my blogs": articles}
        return {"my blogs": [], "message": "You have not created any blogs yet!"}
    raise HTTPException(status_code=404, detail="User not found!")


# - - - - - D E L E T E - A R T I C L E - - - -
@home_routes.delete("/dashboaard/{username}/{title}/delete-blog")
async def delete_blog(username: Annotated[str, Depends(auth_handler.authorize_url)], title: str):
    """
    Delete a blog article from the user's dashboard.

    Parameters:
        username (str): The username of the user.
        title (str): The title of the blog article to be deleted.

    Returns:
        dict: A dictionary containing a message indicating that the article has been deleted.

    Raises:
        HTTPException: If the user or the blog article is not found.
    """
    if username_in_DB(username):
        blog = find_article_by_title(title)
        if blog:
            caches = all_articles_cache()
            with open("blogging_app/all_articles.csv", "w", newline="") as all_articles:
                writer = csv.writer(all_articles)
                writer.writerow(article_header)
                for article in caches:
                    if blog == article:
                        continue
                    else:
                        writer.writerow(article)
            return {"message": "Article deleted!"}
        raise HTTPException(status_code=404, detail=f"No blog with title: {title}!")
    raise HTTPException(status_code=404, detail="User not found!")


# - - - - - D E L E T E - A C C O U N T - - - - -
@home_routes.delete("/delete-account")
async def delete_account(username: Annotated[str, Depends(auth_handler.authorize_url)]):
    """
    Deletes the user account with the specified username.

    Parameters:
        username (str): The username of the account to be deleted.

    Returns:
        dict: A dictionary with a message indicating the success of the deletion.

    Raises:
        HTTPException: If the specified username is not found in the database.
    """
    if username_in_DB(username):
        users = all_users_cache()
        with open("blogging_app/UsersDB.csv", "w", newline="") as UsersDB:
            writer = csv.writer(UsersDB)
            writer.writerow(UsersDB_header)
            for user in users:
                if user[1] == username:
                    continue
                else:
                    writer.writerow(user)
        return {"message": "Account deleted successfully!"}
    raise HTTPException(status_code=404, detail="User not found!")
