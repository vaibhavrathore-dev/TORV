from fastapi import APIRouter
from app.database import users_collection
from app.models.user_model import Users_login,Users_Registration
from passlib.context import  CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "Vaibhav_is_gonna_become_best_dev)"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

auth_router = APIRouter()


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


@auth_router.post("/register")
def register_user(user:Users_Registration):

    existing_user = users_collection.find_one({"email" : user.email})
    if existing_user:
        return {
            "message" : "Email is already registered"
        }
    else:
        new_user = user.model_dump()
        hashed_password = pwd_context.hash(new_user["password"])
        new_user["password"] = hashed_password
        new_user["role"] = "user"
        print(new_user["password"])
        print(type(new_user["password"]))
        result = users_collection.insert_one(new_user)
        return {
            "message" : f"Welcome To Torv , {user.name}" , 
            "user_id" : str(result.inserted_id),
            "role" : "user",
            

        }

@auth_router.post("/login")
def login_user(user : Users_login):
   
    existing_user = users_collection.find_one({"email" : user.email})
    if existing_user:
        entered_password = user.password
        verified = pwd_context.verify(entered_password,existing_user["password"])

        
        if verified == False:
            return {
                "message" : "Invalid password"
            }
        else:
            access_token = create_access_token(
            data={
                "email": existing_user["email"],
                    "role": existing_user["role"]
            }
        )
            return {
                "message" : " Logged in Successfully(30 mins)",
                "access_token": access_token,
                "token_type": "bearer"
            }
    else:
        return{
            "message" : "Invalid Email , Please Regoister as Torv user"
        }
           

