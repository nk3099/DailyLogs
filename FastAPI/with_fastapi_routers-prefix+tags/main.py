from typing import Optional, List
#from pydantic import BaseModel
from fastapi import Body, FastAPI, HTTPException, Response, status
from random import randrange
import psycopg2  #importing psycopg2 to connect to PostgreSQL database
from psycopg2.extras import RealDictCursor  #importing RealDictCursor to get results as dictionaries
import time
from . import schemas  #importing schemas from the same directory
from . import utils
from .routers import post,user

app = FastAPI() #create an instance of FastAPI


# while True:
#   try:
#     conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='Learning@tools1', cursor_factory=RealDictCursor) #connect to the databaseclea
#     cursor = conn.cursor()  #create a cursor to execute SQL queries
#     print("Database connection successful")
#     break  #break the loop if connection is successful
#   except Exception as error:
#     print("Database connection failed")
#     print("Error:", error)
#     time.sleep(2)  #wait for 2 seconds before trying to connect again

#dummy array
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "title of post 2", "content": "content of post 2", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p['id']== id:
            return p
        
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id']==id:
            return i


app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
async def root():
    return {"message": "Hello World from FastAPI!"}


