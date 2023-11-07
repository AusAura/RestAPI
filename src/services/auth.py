from typing import Optional
from icecream import ic
import pickle, redis.asyncio as redis

from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.repository import users as repository_users
from src.conf.config import settings

class Auth:
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    SECRET_KEY = settings.secret_key
    ALGORITHM = settings.algorithm
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/login')
    r = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify the password during loging.

        :param plain_password: Recieved password.
        :type plain_password: str
        :param hashed_password: Stored encrypted password.
        :type hashed_password: str
        :rtype: bool
        """
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, plain_password: str) -> str:
        """
        Encrypts the password during signup.

        :param plain_password: Recieved password.
        :type plain_password: str
        :rtype: str
        """
        return self.pwd_context.hash(plain_password)
    
    async def create_access_token(self, data: dict, expires_delta: Optional[float] = None) -> str:
        """
        Generate new access token.

        :param data: Passed data (email of the user).
        :type data: dict
        :param expires_delta: Optional TTL.
        :type expires_delta: float | None
        :rtype: str
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({'iat': datetime.utcnow(), 'exp': expire, 'scope': 'access token'})
        encoded_access_token = jwt.encode(to_encode, self.SECRET_KEY, self.ALGORITHM)
        return encoded_access_token
    
    async def create_refresh_token(self, data: dict, expires_delta: Optional[float] = None) -> str:
        """
        Generate new refresh token.

        :param data: Passed data (email of the user).
        :type data: dict
        :param expires_delta: Optional TTL.
        :type expires_delta: float | None
        :rtype: str
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)

        to_encode.update({'iat': datetime.utcnow(), 'exp': expire, 'scope': 'refresh token'})
        encoded_refresh_token = jwt.encode(to_encode, self.SECRET_KEY, self.ALGORITHM)
        return encoded_refresh_token
    
    async def create_email_token(self, data: dict, expires_delta: Optional[float] = None) -> str:
        """
        Generate new email token.

        :param data: Passed data (email of the user).
        :type data: dict
        :param expires_delta: Optional TTL.
        :type expires_delta: float | None
        :rtype: str
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)

        to_encode.update({'iat': datetime.utcnow(), 'exp': expire, 'scope': 'email token'})
        encoded_email_token = jwt.encode(to_encode, self.SECRET_KEY, self.ALGORITHM)
        return ic(encoded_email_token)
    
    async def decode_refresh_token(self, refresh_token: str):
        """
        Decode refresh token and return the user's email. Raise errors if invalid token or scope.

        :param refresh_token: Passed token.
        :type refresh_token: str
        :rtype: str
        """
        try:
            payload = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'refresh token':
                email = payload['sub']
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Scope')
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Cannot validate')
        
    async def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        """
        Decode access token and return the user. Raise errors if invalid token or scope, wrong email or user. Stores the request for user in Redis cache.

        :param token: Passed token.
        :type token: str
        :rtype: User
        """
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
        
        user = ic(await self.r.get(f'user:{email}'))
        if user is None:
            user = await repository_users.get_user_by_email(email, db)
            if user is None:
                raise credentials_exception
            ic(await self.r.set(f'user:{email}', pickle.dumps(user)))
            await self.r.expire(f'user:{email}', 900)
        else:
            user = ic(pickle.loads(user))

        return user
    
    async def get_email_from_token(self, email_token: str) -> str:
        """
        Decode email token and returns it. Raise errors if unprocessable token.

        :param token: Passed token.
        :type token: str
        :rtype: str
        """
        try:
            payload = jwt.decode(email_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email = payload["sub"]
            return email
        except JWTError as e:
            ic(e)
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                          detail="Invalid token for email verification")  
        

    async def reset_password(self, email: str, email_token: str, db: Session) -> None:
        """
        Create (on inner algorithm) and set new password for the user in DB. Raise error if user with passed email not found.

        :param email: Passed email of the user.
        :type email: str
        :param email_token: Passed email token.
        :type email: str
        :param db:
        :type db: Session
        :rtype: None
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Wrong credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
                
        user = await repository_users.get_user_by_email(email, db)
        if user is None:
            raise credentials_exception
        
        user.password = self.get_password_hash(email_token)
        user.refresh_token
        user.refresh_token = await self.create_refresh_token(data={"sub": email})
        db.commit()

    
auth_service = Auth()