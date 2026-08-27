import os
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime,timedelta
from fastapi import HTTPException

SECRET=os.getenv('SECRET', 'arv@h2so4')
ALGORITHM=os.getenv('ALGORITHM', 'HS256')
print(SECRET,ALGORITHM)

oauth=OAuth2PasswordBearer(tokenUrl='reglog')

def create_token(user:str):
    payload={
        'sub':user,
        'exp':datetime.now()+timedelta(hours=1)
    }
    return jwt.encode(payload,SECRET,ALGORITHM) #type:ignore

def get_by_token(token:str):
    try:
        data=jwt.decode(token,SECRET,algorithms=[ALGORITHM]) #type:ignore
        return data['sub']
    except:
        raise HTTPException(401, 'Вы не зарегистрированы или проблема с токеном')