from pydantic import BaseModel
from typing import List, Optional
import datetime


# User Sign-in
class User(BaseModel):
    id: str
    username: str
    first_name: str
    last_name: str
    email: str
    password: str

class Articles(BaseModel):
    title: str
    author: str
    content: str
    date_published: str

class UpdateArticle(BaseModel):
    title: str
    content: str

class UpdateArticleResponse(BaseModel):
    title: str
    author: str
    content: str
    date_published: str
    last_updated: str

class SocialMediaLinks(BaseModel):
    twitter: str | None = " "
    facebook: str | None = " "
    instagram: str | None = " "

class UserProfile(User, SocialMediaLinks):
    bio: Optional[str | None] = "Write something about yourself!"
    website: str | None = " "
    last_updated_at: str
    posts: List[Articles]
    posts_count: int