from passlib.context import CryptContext #ie. for hashing the password -> in FastAPI security section : OAuth2 wiht password(and hashing)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #create a password context for hashing passwords

def hash(password: str):
    return pwd_context.hash(password)  #hash the password using bcrypt

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)  #verify the password against the hashed password