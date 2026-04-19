from fastapi import FastAPI,status,Body
import logging
app=FastAPI()

@app.get("/") 
def welcom():
    return {"message":"welcome to Sprinklr"}
    
users=[]

@app.get("/users")
def get_users():
    return {"users are": users}

"""
If we don't use Pydantic model
Then,we must clearly tell FastAPI where the data comes from - query param or request body"""

# #POST http://127.0.0.1:8000/create_user?user=Neeraj    
@app.post("/create_user", status_code=status.HTTP_201_CREATED)
def create_user(user: str):
    logging.info(f"User created: {user}")

    users.append(user)
    return {"message":f"{user} is created successfully"}


@app.delete("/delete_user/{user}")
def delete_user(user:str):
    if user in users:
        users.remove(user)
        return {"message":f"{user} is deleted successfully"}
    else:
        return {"message":f"{user} not found in the list of users"}

#POST http://127.0.0.1:8000/create_user
#"Neeraj"
# @app.post("/create_user", status_code=status.HTTP_201_CREATED)
# def create_user(user: str = Body(...)):
#     logging.info(f"User created: {user}")
#     users.append(user)
#     return {"message":f"{user} is created successfully"}

""" 
Pydantic is a library used by FastAPI to:

validate data ✅
parse data ✅
enforce types ✅

Think of it like a strict data checker.

------------------How FastAPI decides: query vs body?-------------------------------------
Rule 1: Simple types → Query parameters
def create_user(user: str):

👉 user is treated as a query parameter

Call like:
POST /create_user?user=Neeraj

Rule 2: Pydantic model → Request body
def create_user(user: User):

👉 user is treated as JSON body

Call like:

{
  "name": "Neeraj",
  "age": 25
}


"""


#Terminal 1 → run server
#uvicorn main:app --reload

#Terminal 2 → send request
#curl -X POST "http://127.0.0.1:8000/create_user?user=Neeraj

