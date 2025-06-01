

from .. import schemas
from typing import Optional, List
from fastapi import Body, FastAPI, HTTPException, Response, status, APIRouter, Depends
#from ..database import cursor, conn  #importing cursor and conn from database.py to execute SQL queries -> if doing Global conn/cursor 
from ..database import get_db  #importing get_db function to get database connection
from .. import oauth2


router = APIRouter(
    prefix='/posts',  #prefix for all routes in this router - as all routes in this post.py file were starting with /posts
    tags=['Posts'] #tags used to group the routes in the OpenAPI documentation - http://127.0.0.1:8000/docs

)  #creating a router object to handle post-related routes


#Now, retrieve data from database.
@router.get("/",response_model=List[schemas.postResponse])
def get_posts(conn = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)):  #conn is a dependency that gets the database connection
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM posts""")
    my_posts = cursor.fetchall()
    return  my_posts 


#If to protect this endpoint with authentication, i.e. the user must be logged in to create a post - we want they provide access_token, 
#thereofore we can use Depends(oauth2.get_current_user) as a dependency in the function signature.
@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.postResponse) #status code 201 Created
def create_posts(payload: schemas.validate_postCreate, conn = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)): 
   
   cursor =  conn.cursor()
   #cursor.execute(f""" INSERT INTO posts (title,content,published) VALUES ({posts.title},{posts.content},{posts.published})""") #this aslo works, but it is not safe against SQL injection attacks
   cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (payload.title, payload.content, payload.published))
   new_post = cursor.fetchone()  #fetch the newly created post
   conn.commit()  #commit the changes to the database
   return new_post



@router.get("/{id}", response_model=schemas.postResponse) #id -> path parameter in the URL, note: it always gets returned as a string, therefore we convert it to int
def get_post(id : int, conn = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)): #Type hint tells FastAPI to validate the input
   cursor = conn.cursor()
   cursor.execute("""SELECT * FROM posts WHERE id=%s""",(str(id),)) #extra comma is needed to make it a tuple
   #ie. The second argument to cursor.execute(query, params) must be a tuple or sequence of parameters. Even if there's just one parameter, like id, it must still be passed as a tuple — hence the comma.
   post = cursor.fetchone()  #fetch the post with the given id
   if not post:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

   return post



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT) #status code 204 No Content
def delete_post(id: int, conn = Depends(get_db),user_id : int = Depends(oauth2.get_current_user)):
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""", (str(id),))  #delete the post with the given id
    deleted_post = cursor.fetchone()  #fetch the deleted post
    conn.commit()

    if deleted_post is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)  



@router.put("/{id}",response_model=schemas.postResponse)
def update_post(id:int, post: schemas.validate_postCreate, conn = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)):

    cursor = conn.cursor()

    cursor.execute(""" UPDATE posts SET title=%s,  content=%s, published=%s WHERE id=%s RETURNING *""",(post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    

    return updated_post  #return the updated post
