from typing import OptionalAdd commentMore actions
from fastapi import Body, FastAPI
from pydantic import BaseModel #Pydantic is data validation library for Python.


app = FastAPI() #create an instance of FastAPI

class validate_post(BaseModel):
    title:str
    content:str
    published:bool = True  # Default value is True
    #rating:float = None  # Default value is None, meaning it can be optional
    #OR 
    rating:Optional[float]=None  # This is another way to define an optional field using Optional from typing module

# The validate_post class is a Pydantic model that defines the structure of the data
# that we expect to receive in the request body when creating a post.
# It has four fields: title, content, published, and rating.
# title and content are required fields, while published has a default value of True
# and rating has a default value of None, meaning it is optional.
# FastAPI will automatically validate the data against this model when we receive a POST request.

@app.get("/")
async def root():
    return {"message": "Hello World from FastAPI!"}

@app.get("/posts")
def get_posts():
    return {"data": "This is a post"}

# @app.post("/createposts")
# def create_posts(payload: dict=Body(...)): //to retrieve data from the request body (of Post method which we passed)
#     print(payload)
#     return {"new_post": f"post created with title : {payload['title']} and content : {payload['content']}"}

@app.post("/createposts")
def create_posts(payload: validate_post):
    # payload is an instance of validate_post, which is a Pydantic model and it will automatically validate the data against the model
    # If the data is valid, it will be passed to the function
    # If the data is invalid, FastAPI will return a 422 Unprocessable Entity error
    # payload is a Pydantic model instance, so you can access its attributes directly - For example, payload.title, payload.content, etc.
    print(payload)
    print(payload.dict())
    print(payload.title)Add commentMore actions
    return {"new_post": payload}
    #return {"new_post": "created"}
