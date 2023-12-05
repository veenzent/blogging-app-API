from fastapi import APIRouter, Form, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated, Optional
from blogging_app import schemas, models
from blogging_app.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from blogging_app.auth import auth_handler


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
async def get_latest_blogs(db: Session = Depends(get_db)):
    """
    Retrieves the latest blogs from the articles database file.

    Returns:
    dict: A dictionary containing the latest blogs, where the keys are the blog titles and the values are the corresponding blog articles.
    """
    latest = db.query(models.Articles).all()
    return latest

    # with open("blogging_app/all_articles.csv", "r") as all_articles:
    #     reader = csv.reader(all_articles)
    #     next(reader)
    #     reader = sorted(reader, key=lambda x: x[3], reverse=True)
    #     trending = []
    #     for i, article in enumerate(reader):
    #         if i <= 4:
    #             article = schemas.Articles(title=article[0], author=article[1], content=article[2], date_published=article[3])
    #             trending.append(article)
    # return{"Latest Blogs": trending}


# - - - - - S I G N - U P - - - - -
@home_routes.post("/sign-up")
async def sign_up(
  username: Annotated[str, Form(max_length=100)],
  first_name: Annotated[str, Form(max_length=100)],
  last_name: Annotated[str, Form(max_length=100)],
  email: Annotated[str, Form(max_length=100)],
  password: Annotated[str, Form(max_length=100)],
  confirm_password: Annotated[str, Form(max_length=100)],
  db: Annotated[Session, Depends(get_db)],
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
    username_in_DB_update = db.query(models.User).filter(models.User.username == username).first()
    email_in_DB_update = db.query(models.User).filter(models.User.email == email).first()
    if confirm_password != password:
        raise HTTPException(status_code=400, detail="Passwords do not match!")
    if username_in_DB_update:
        raise HTTPException(status_code=400, detail="Username already exists!")
    if email_in_DB_update:
        raise HTTPException(status_code=400, detail="Email already exists!")
    else:
        user = models.User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email, 
            password=auth_handler.get_password_hash(password),
            last_updated_at=datetime.strptime(datetime.now().strftime("%d-%m-%Y %H:%M:%S"), "%d-%m-%Y %H:%M:%S").strftime("%d-%B-%Y %H:%M:%S")
        )
        try:
            db.add(user)
            db.commit()
            db.refresh(user)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail="Internal server error")
    return {"message": "Sign-up successful!."}


# - - - - - L O G I N / S I G N - I N- - - - - -
@home_routes.post("/token", response_model=schemas.Token)
async def sign_in(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
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

    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if user.password and auth_handler.verify_password(form_data.password, user.password):
        access_token_expires = timedelta(minutes=auth_handler.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth_handler.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    else:
        raise credential_exception
    return {"access_token": access_token, "token_type": "bearer"}


# - - - - - U P D A T E - P R O F I L E - - - - -
@home_routes.put("/dashboard/{username}/update-profile", response_model=schemas.UserProfileResponse)
async def update_profile(
    username: Annotated[str, Depends(auth_handler.authorize_url)],
    bio: Optional[Annotated[str | None, Form(default="Write something about yourself!")]],
    website: Optional[Annotated[str, Form()]],
    twitter: Optional[Annotated[str, Form()]],
    facebook: Optional[Annotated[str, Form()]],
    instagram: Optional[Annotated[str, Form()]],
    db: Session = Depends(get_db)
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
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        user.bio = bio
        user.website = website
        user.twitter = twitter
        user.facebook = facebook
        user.instagram = instagram
        user.posts = db.query(models.Articles).filter(models.Articles.author_username == user.username).all()
        user.posts_count = len(user.posts)
        user.last_updated_at = datetime.strptime(datetime.now().strftime("%d-%m-%Y %H:%M:%S"), "%d-%m-%Y %H:%M:%S").strftime("%d-%B-%Y %H:%M:%S")

        updated_profile = {
            "id":user.user_id,
            **user.__dict__
        }

        try:
            db.commit()
            db.refresh(user)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail="Internal server error")
        return updated_profile
    raise HTTPException(status_code=404, detail="User not found!")


# - - - - - M Y - P R O F I L E - - - - -
@home_routes.get("/dashboard/profile", response_model=schemas.UserProfileResponse)
async def my_profile(username: Annotated[str, Depends(auth_handler.authorize_url)], db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        user.posts = db.query(models.Articles).filter(models.Articles.author_username == user.username).all()
        user.posts_count = len(user.posts)
        user.last_updated_at = datetime.strptime(str(user.last_updated_at), "%Y-%m-%d %H:%M:%S").strftime("%d-%B-%Y %H:%M:%S")
        
        profile = {
            "id": user.user_id,
            **user.__dict__
        }
        return profile
    raise HTTPException(status_code=404, detail="User not found!")


# - - - - - C R E A T E - B L O G - - - - -
@home_routes.post("/create-blog", response_model=schemas.Articles)
async def create_blog(
    username: Annotated[str, Depends(auth_handler.authorize_url)],
    title: Annotated[str, Form()],
    content: Annotated[str, Form(...)],
    db: Session = Depends(get_db)
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
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        author = f"{user.first_name} {user.last_name}"
        article = models.Articles(
            title = title,
            author = author,
            author_username = user.username,
            content = content,
            date_published = datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            # last_updated = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        )
        try:
            db.add(article)
            db.commit()
            db.refresh(article)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail="Internal server error")
        print(article.id)
        print(article.title)
        created_article = schemas.Articles(
            id = article.id,
            title = article.title,
            author = article.author,
            content = article.content,
            date_published = datetime.strptime(str(article.date_published), "%Y-%m-%d %H:%M:%S").strftime("%d-%B-%Y %H:%M:%S")
        )
        
        return created_article
    raise HTTPException(status_code=404, detail="User not found, Sign up to start writing blogs!")


# - - - - - E D I T - A R T I C L E - - - - -
@home_routes.put("/dashboaard/{username}/edit-blog", response_model=schemas.UpdateArticleResponse)
async def edit_blog(username: Annotated[str, Depends(auth_handler.authorize_url)], article_id: int, update: schemas.UpdateArticle, db: Session = Depends(get_db)):
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
    article = db.query(models.Articles).filter(models.Articles.id == article_id).first()
    if article:
        article.title = update.title
        article.content = update.content
        article.last_updated = datetime.today().strftime("%d-%B-%Y %H:%M:%S")

        updated_article = {
            "id": article.id,
            "title": article.title,
            "content": article.content,
            "author": article.author,
            "date_published": datetime.strptime(str(article.date_published), "%Y-%m-%d %H:%M:%S").strftime("%d-%B-%Y %H:%M:%S"),
            "last_updated": article.last_updated
        }

        try:
            db.commit()
            db.refresh(article)
        except Exception as e:
            db.rollback()
            print(e)
            raise HTTPException(status_code=500, detail="Internal server error")

        return updated_article
    raise HTTPException(status_code=404, detail="Article not found!")


# - - - - - M Y - B L O G S - - - - -
@home_routes.get("/dashboaard/{username}/my-blogs")
async def my_blogs(username: Annotated[str, Depends(auth_handler.authorize_url)], db: Session = Depends(get_db)):
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
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        author = f"{user.first_name} {user.last_name}"
        my_blogs = db.query(models.Articles).filter(models.Articles.author == author).all()
        return my_blogs
    raise HTTPException(status_code=404, detail="User not found!")


# - - - - - D E L E T E - A R T I C L E - - - -
@home_routes.delete("/dashboaard/{username}/{id}/delete-blog")
async def delete_blog(username: Annotated[str, Depends(auth_handler.authorize_url)], article_id: int, db: Session = Depends(get_db)):
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
    article = db.query(models.Articles).filter(models.Articles.id == article_id).first()

    if article:
        db.delete(article)
        db.commit()
        return {"message": "Article deleted successfully!"}
    
    raise HTTPException(status_code=404, detail=f"No Article with specified id: {article_id}!")


# - - - - - D E L E T E - A C C O U N T - - - - -
@home_routes.delete("/delete-account")
async def delete_account(username: Annotated[str, Depends(auth_handler.authorize_url)], db: Session = Depends(get_db)):
    """
    Deletes the user account with the specified username.

    Parameters:
        username (str): The username of the account to be deleted.

    Returns:
        dict: A dictionary with a message indicating the success of the deletion.

    Raises:
        HTTPException: If the specified username is not found in the database.
    """
    user = db.query(models.User).filter(models.User.username == username).first()

    if user:
        db.delete(user)
        db.commit()
        return {"message": "Account deleted successfully!"}
    raise HTTPException(status_code=404, detail="User not found!")
