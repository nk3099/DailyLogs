from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  #OAuth2PasswordBearer is a class that provides a way to get the token from the request

#SECRET_KEY,
#Algorithm,
#Expriation time - ie. for how long the user logged in.

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 0.5

def create_access_token(data :  dict): #as access_token will have payload(i.e whatever data we want to encode in the token)
   to_encode =  data.copy() #copying the data to avoid modifying the original data

   expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
   to_encode.update({"exp": expire})  #ie. encoding the extra property - expiration time - that we want to encode in the JWT token
   
   #to_encode.update({"expiration":expire})
   """TypeError: Object of type datetime is not JSON serializable
   passing a datetime object (likely an expiration time) directly into the JWT payload, 
   and json.dumps() (used under the hood by python-jose) cannot serialize datetime objects by default.
   
   If expire is a datetime object, you need to convert it to a timestamp or ISO format."""

   encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

   return encoded_jwt


def verify_access_token(token: str, credentials_exception):
   try :
     payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM]) #decoding the token to verify it
     id : str = payload.get("user_id")
     if id is None:
        raise credentials_exception  
     token_data = schemas.TokenData(id=id) 
   except JWTError:
        raise credentials_exception
   
   return token_data  #returning the token data, which contains the user id extracted from the token payload
   

#this get_curretn_user function will call the verify_access_token function to verify the token and return the user data
def get_current_user(token: str = Depends(oauth2_scheme)):
   credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})  
   return verify_access_token(token, credentials_exception)  #verifying the token and returning the user data




""" Note: usage of this get_current_user in post.py file: for "/post" route as below:"""
#If to protect this endpoint with authentication, i.e. the user must be logged in to create a post - we want they provide access_token, 
#thereofore we can use Depends(oauth2.get_current_user) as a dependency in the function signature.
"""
@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.postResponse) #status code 201 Created
def create_posts(payload: schemas.validate_postCreate, conn = Depends(get_db), get_current_user : int = Depends(oauth2.get_current_user)): 
........
"""