from pydantic import BaseModel
from typing import List, Annotated
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
    last_updated: datetime.datetime

class SocialMediaLinks(BaseModel):
    twitter: str | None = None
    facebook: str | None = None
    instagram: str | None = None

class UserProfile(BaseModel):
    user: User
    bio: str | None = "Write something about yourself!"
    avatar_url: str | None = None
    website_url: str | None = None
    social_media_links: SocialMediaLinks
    acct_created_at: datetime.datetime
    last_updated_at: datetime.datetime
    following_count: int
    follower_count: int
    post_count: int
    comment_count: int
    posts: List[Articles]