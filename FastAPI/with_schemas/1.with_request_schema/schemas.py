from pydantic import BaseModel 

class validate_postBase(BaseModel):
    title:str
    content:str
    published:bool = True  

class validate_postCreate(validate_postBase): #inherits from validate_postBase
    pass

