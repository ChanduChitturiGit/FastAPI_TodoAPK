from pydantic import BaseModel,Field

class User(BaseModel):
    email : str 
    username : str
    password : str = Field(min_length=4)
    
class token_data(BaseModel):
    access_token : str
    token_type : str
    
class Todos(BaseModel):
    task : str
    description : str
    priority : int
    complete : bool = Field(default=False)
