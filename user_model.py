from pydantic import BaseModel

class Users_Registration(BaseModel):
    name : str
    email : str
    password : str
    role : str

class Users_login(BaseModel):
    email : str
    password : str