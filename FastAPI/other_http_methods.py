from typing import Optional
from fastapi import Body, FastAPI, HTTPException, Response, status
from pydantic import BaseModel 
from random import randrange

app = FastAPI() #create an instance of FastAPI

class validate_post(BaseModel):
    title:str
    content:str
    published:bool = True  
    rating:Optional[float]=None  

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

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code = status.HTTP_201_CREATED) #status code 201 Created
def create_posts(payload: validate_post):
   payload_dict = payload.dict()
   payload_dict['id'] = randrange(0,1000000)  # Assign a random ID
   my_posts.append(payload_dict)
   return {"data": payload_dict}

# @app.get("/posts/{id}") #id -> path parameter in the URL, note: it always gets returned as a string, therefore we convert it to int
# def get_post(id):
#    post = find_post(int(id))
#    return {"post_detail": post}


# would return error if:
# 1) def get_post(id) --> 500 Internal Server Error if int(id) fails manually. (ie. when string is passed instead of int)
# 2) def get_post(id: int) --> ✅ 422 Unprocessable Entity automatically on bad input
# 3) try/except with HTTPException --> ✅ 400 Bad Request or custom error

# A 500 Internal Server Error means:
# ⚠️ The server encountered an unexpected condition that prevented it from fulfilling the request.

# 422 Unprocessable Entity error in FastAPI (and generally in web APIs) means:
# ✅ The request was well-formed (valid JSON, correct HTTP method, etc.),
# ❌ But the data was semantically incorrect or failed validation.




@app.get("/posts/{id}") #id -> path parameter in the URL, note: it always gets returned as a string, therefore we convert it to int
def get_post(id : int, response_variable : Response): #Type hint tells FastAPI to validate the input
   post = find_post(int(id))
   if not post:
         #response_variable.status_code = 404
         response_variable.status_code =  status.HTTP_404_NOT_FOUND
         return {"message": f"Post with id {id} not found"}
         #OR
         #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

   return {"post_detail": post}



#Suppose:
# @app.get("/posts/latest")
# def get_latest_post():
#     latest_post = my_posts[len(my_posts)-1]
#     return {"latest_post": latest_post}

# Ordering of API endpoints matters:
# @app.get("/posts/{id}")
# @app.get("/posts/latest")
# as in the above example, we have defined the endpoint for /posts/{id} before the /posts/latest endpoint,
# therefore it would go from top-to-bottom to match the route with /posts/some_variable first -> this would result in the /posts/latest endpoint being unreachable 
# because FastAPI would match the /posts/{id} endpoint first for any request that includes an ID.
# To avoid this, we can either change the order of the endpoints or use a different path route. example: @app.get("/posts/id/{id}")



@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT) #status code 204 No Content
def delete_post(id: int):
    #deleting post
    #find the index in the array that has the required ID 
    #my_posts.pop(index) #remove the post from the array
    index = find_index_post(id)

    if index is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    #If deleting a post that does not exist, we get TypeError: 'NoneType' object cannot be interpreted as an integer
    #therefore, we can return a 404 Not Found error.

    my_posts.pop(index)

    return Response(status_code=status.HTTP_204_NO_CONTENT)  #returning 204 No Content status code -> as not to send any content back to the client
    #else we get LocalProtocolError: Too much data declared for Content-Length



@app.put("/posts/{id}" )
def update_post(id:int, post: validate_post):
    print(post)
    index = find_index_post(id)

    if index is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    
    post_dict = post.dict()  #convert the Pydantic model to a dictionary
    post_dict['id'] = id
    my_posts[index]=post_dict  #update the post in the array

    return{"data": post_dict}  #return the updated post
