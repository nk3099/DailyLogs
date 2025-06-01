from typing import Optional
from fastapi import Body, FastAPI, HTTPException, Response, status
from pydantic import BaseModel 
from random import randrange
import psycopg2  #importing psycopg2 to connect to PostgreSQL database
from psycopg2.extras import RealDictCursor  #importing RealDictCursor to get results as dictionaries
import time
#from . import schemas  #importing schemas from the same directory

app = FastAPI() #create an instance of FastAPI

class validate_post(BaseModel):
    title:str
    content:str
    published:bool = True  

while True:
  try:
    conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='Learning@tools1', cursor_factory=RealDictCursor) #connect to the databaseclea
    cursor = conn.cursor()  #create a cursor to execute SQL queries
    print("Database connection successful")
    break  #break the loop if connection is successful
  except Exception as error:
    print("Database connection failed")
    print("Error:", error)
    time.sleep(2)  #wait for 2 seconds before trying to connect again

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

@app.get("/")
async def root():
    return {"message": "Hello World from FastAPI!"}


#Now, retrieve data from database.
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    my_posts = cursor.fetchall()
    return {"data": my_posts }

@app.post("/posts", status_code = status.HTTP_201_CREATED) #status code 201 Created
def create_posts(payload: validate_post):
   #cursor.execute(f""" INSERT INTO posts (title,content,published) VALUES ({posts.title},{posts.content},{posts.published})""") #this aslo works, but it is not safe against SQL injection attacks
   cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (payload.title, payload.content, payload.published))
   new_post = cursor.fetchone()  #fetch the newly created post
   conn.commit()  #commit the changes to the database
   return {"data": new_post}



@app.get("/posts/{id}") #id -> path parameter in the URL, note: it always gets returned as a string, therefore we convert it to int
def get_post(id : int): #Type hint tells FastAPI to validate the input
   cursor.execute("""SELECT * FROM posts WHERE id=%s""",(str(id),)) #extra comma is needed to make it a tuple
   #ie. The second argument to cursor.execute(query, params) must be a tuple or sequence of parameters. Even if there's just one parameter, like id, it must still be passed as a tuple — hence the comma.
   post = cursor.fetchone()  #fetch the post with the given id
   if not post:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

   return {"post_detail": post}



@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT) #status code 204 No Content
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""", (str(id),))  #delete the post with the given id
    deleted_post = cursor.fetchone()  #fetch the deleted post
    conn.commit()

    if deleted_post is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)  



@app.put("/posts/{id}" )
def update_post(id:int, post: validate_post):

    cursor.execute(""" UPDATE posts SET title=%s,  content=%s, published=%s WHERE id=%s RETURNING *""",(post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")

    return{"data": updated_post}  #return the updated post
