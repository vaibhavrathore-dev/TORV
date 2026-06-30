from fastapi import HTTPException, Depends 
from fastapi.security import OAuth2PasswordBearer 
from jose import jwt, JWTError

SECRET_KEY = "Vaibhav_is_gonna_become_best_dev)"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token : str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        email = payload.get("email")
        role = payload.get("role")
        if email is None:
            raise HTTPException(status_code = 401 , detail = "Invalid Token")
        
        return {
                "email" : email,
                "role" : role
            }
    except JWTError:
        raise HTTPException(status_code=401 , detail = "Invalid Token or Session Expired")
    
def admin_required(role = Depends(get_current_user)):
    if role["role"] != "admin":
        raise HTTPException(status_code=403,detail = "Only allowed for admin")
    else:
        return {
            "message" : "Acess granted"\
        }
    

