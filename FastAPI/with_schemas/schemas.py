from pydantic import BaseModel 

class validate_post(BaseModel):
    title:str
    content:str
    published:bool = True  