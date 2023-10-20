from pydantic import BaseModel
from typing import List
import datetime


# User Sign-in
class User(BaseModel):
    id: str
    username: str
    first_name: str
    last_name: str
    email: str
    password: str

class CreateArticle(BaseModel):
    title: str
    content: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    author: str

class Articles(BaseModel):
    title: str
    author: str
    content: str
    date_pblished: str

all_articles: List[Articles] = []

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
    posts: List[CreateArticle]