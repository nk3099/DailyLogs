from pydantic import BaseModel 
from datetime import datetime

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