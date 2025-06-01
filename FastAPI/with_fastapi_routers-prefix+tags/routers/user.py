
from .. import schemas, utils
from fastapi import Body, FastAPI, HTTPException, Response, status, APIRouter, Depends
#from ..database import cursor, conn  #importing cursor and conn from database.py to execute SQL queries -> if doing Global conn/cursor 
from ..database import get_db  #importing get_db function to get database connection

router = APIRouter(
    prefix='/users', #prefix for all routes in this router - as all routes in this user.py file were starting with /users
    tags=['Users'] #tags used to group the routes in the OpenAPI documentation - http://127.0.0.1:8000/docs
) #creating a router object to handle user-related routes

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, conn = Depends(get_db)):
    cursor = conn.cursor()
    #hash the password - that can be retrieved from user.password
    
    hashed_password = utils.hash(user.password) #OR hashed_password = pwd_context.hash(user.password)  #hash the password using bcrypt
    #Note: utils.hash is a function that hashes the password using bcrypt, defined in utils.py
    user.password = hashed_password


    cursor.execute("""INSERT INTO users(email,password) VALUES(%s,%s) RETURNING *""", (user.email,user.password))
    new_user = cursor.fetchone()
    conn.commit()

    return new_user


@router.get("/{id}",response_model = schemas.UserOut)
def get_user(id: int, conn = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM users WHERE id=%s """,(str(id),))
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")

    return user