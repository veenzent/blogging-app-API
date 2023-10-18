from pydantic import BaseModel
from typing import List
import datetime


# User Sign-in
class SignIn(BaseModel):
    email: str
    password: str

class Article(BaseModel):
    title: str
    content: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    # author: get author name from class User

class SocialMediaLinks(BaseModel):
    twitter: str | None = None
    facebook: str | None = None
    instagram: str | None = None

class User(BaseModel):
    id: int
    username: str
    email: str
    name: str
    bio: str | None = "Write something about yourself!"
    avatar_url: str | None = None
    website_url: str | None = None
    social_media_links: SocialMediaLinks
    acct_created_at: datetime.datetime
    last_updated_at: datetime.datetime
    role: str
    following_count: int
    follower_count: int
    post_count: int
    comment_count: int
    posts: List[Article]