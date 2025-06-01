from fastapi import APIRouter, Depends, HTTPException, status, Response
from ..database import get_db
from .. import schemas, utils, oauth2


router = APIRouter(
    tags=['Authentication']
)

#would be post request as user would hv to provide their credentials (username and password) to log in - ie. send data.
@router.post("/login", response_model=schemas.Token)
def login(user_credentials: schemas.UserLogin, conn = Depends(get_db) ):
    cursor=conn.cursor()

    cursor.execute("""SELECT * FROM users WHERE email=%s""", (str(user_credentials.email),)) #fetch user with the given email
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user['password']): #hashed_password stored in database, ie. in user.password
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    #create token
    #access_token = oauth2.create_access_token(data = {"userd_id": user.id}) => AttributeError: 'RealDictRow' object has no attribute 'id'
    """user object is a RealDictRow, meaning it functions like a dictionary—so you should access its fields 
    using key-based syntax (e.g., user["password"]) rather than attribute-style dot notation (e.g., user.password)."""


    access_token = oauth2.create_access_token(data={"user_id": user['id']})
    #OR 
    #access_token = oauth2.create_access_token(data={"user_id": user.get('id')})  #using get() method to avoid KeyError if 'id' is not present


    #return token
    return {"access_token":access_token, "token_type": "bearer"}


   
