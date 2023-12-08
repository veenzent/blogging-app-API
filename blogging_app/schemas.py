from datetime import datetime
from fastapi import Form
from pydantic import BaseModel
from typing import List, Optional, Annotated





class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

# User Sign-in
class User(BaseModel):
    id: str
    username: str
    first_name: str
    last_name: str
    email: str
    password: str

class LatestArticleResponse(BaseModel):
    title: str
    author: str
    content: str
    date_published: str
    last_updated: str

class Articles(BaseModel):
    id: int
    title: str
    author: str
    content: str
    date_published: str

    class Config:
        from_attributes = True

class UpdateArticle(BaseModel):
    title: str
    content: str

class UpdateArticleResponse(UpdateArticle):
    id: int
    author: str
    date_published: str
    last_updated: str

class SocialMediaLinks(BaseModel):
    twitter: str | None = " "
    facebook: str | None = " "
    instagram: str | None = " "

class UserProfile(User, SocialMediaLinks):
    bio: Optional[Annotated[str, None, Form(default="Write something about yourself!")]]
    website: str | None = " "
    last_updated_at: datetime
    posts: List[Articles] = []
    posts_count: int

    class Config:
        from_attributes = True

class UserProfileResponse(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: str
    password: str
    bio: Optional[Annotated[str, None, Form(default="Write something about yourself!")]]
    website: str | None = " "
    twitter: str | None = " "
    facebook: str | None = " "
    instagram: str | None = " "
    last_updated_at: str
    posts: List[Articles] = []
    posts_count: int