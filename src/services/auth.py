from typing import Optional
from icecream import ic

from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.repository import users as repository_users

class Auth:
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    SECRET_KEY = 'Some_key'
    ALGORITHM = 'HS256'
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/login')

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, plain_password: str) -> str:
        return self.pwd_context.hash(plain_password)
    
    async def create_access_token(self, data: dict, expires_delta: Optional[float] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({'iat': datetime.utcnow(), 'exp': expire, 'scope': 'access token'})
        encoded_access_token = jwt.encode(to_encode, self.SECRET_KEY, self.ALGORITHM)
        return encoded_access_token
    
    async def create_refresh_token(self, data: dict, expires_delta: Optional[float] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)

        to_encode.update({'iat': datetime.utcnow(), 'exp': expire, 'scope': 'refresh token'})
        encoded_refresh_token = jwt.encode(to_encode, self.SECRET_KEY, self.ALGORITHM)
        return encoded_refresh_token
    
    async def decode_refresh_token(self, refresh_token: str) -> None:
        try:
            payload = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'refresh token':
                email = payload['sub']
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Scope')
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Cannot validate')
        
    async def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Wrong credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )

        ic(token)
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if ic(payload['scope']) == 'access token':
                email = payload['sub']
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
            
        except JWTError as e:
            ic('it is a JWT', e)
            raise credentials_exception
        
        user = await repository_users.get_user_by_email(email, db)
        if user is None:
            raise credentials_exception
        return user
    
auth_service = Auth()