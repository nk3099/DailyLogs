from pydantic import BaseModel, EmailStr 
from datetime import datetime
from typing import Optional

class validate_postBase(BaseModel):
    title:str
    content:str
    published:bool = True  

class validate_postCreate(validate_postBase): #inherits from validate_postBase
    pass

#for configuring how the response from the API should look like
class postResponse(validate_postBase): #inherits title,content,published from validate_postBase
    id: int
    created_at: datetime

# OR as below:
# class postResponse(BaseModel): 
#     id: int
#     title: str
#     content: str
#     published: bool
#     created_at: datetime

"""
UseCase of postResponse:
When we create a post, we want to return only the title, content, and published status of the post, not the id and created_at fields.
example: for now in get_request we get:
{
        "id": 1,
        "title": "first_post",
        "content": "welcome to first_post!",
        "published": true,
        "created_at": "2025-05-31T16:04:04.886711+05:30"
    },
so, want to limit the response to only title, content and published
and not include id and created_at
"""





#had to do this: pip install --upgrade email-validator pydantic
#else was giving AttributeError: 'ValidatedEmail' object has no attribute 'normalized'
class UserCreate(BaseModel):
    email: EmailStr
    password: str


#when we want to send back the user data (without password) to the clien that requested it, ie. the response from the API should look like
class UserOut(BaseModel):
    id : int
    email: EmailStr
    created_at: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel): #schema for token data -> i.e the data we embed into our access_token
    id: Optional[int] = None