# from typing import List
from icecream import ic

from fastapi import APIRouter, HTTPException, Depends, status, Security
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from fastapi import BackgroundTasks
# from pydantic import EmailStr

from fastapi_limiter.depends import RateLimiter

from src.database.db import get_db
from src.schemas import UserModel, UserResponce, TokenModel, RequestEmail
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.services.email import send_verification, send_reset
# from src.services.email import EmailSchema

router = APIRouter(prefix='/auth', tags=['auth'])
security = HTTPBearer()
# bg_tasks = BackgroundTasks()


@router.post('/signup', response_model=UserResponce, status_code=status.HTTP_201_CREATED, description='No more than 2 requests per minute',
            dependencies=[Depends(RateLimiter(times=2, seconds=60))])
async def signup(body: UserModel, db: Session = Depends(get_db)):
    """
    Signup user.

    :param body: The passed data for signup.
    :type body: UserModel
    :param db:
    :type db: Session
    :rtype: JSON
    """
    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Already exists')
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, db)

    # background_tasks.add_task(send_verification, new_user.email, new_user.username)
    # e_body = ic(EmailSchema(email=body.email))                       
    
    if not await ic(send_verification(new_user.email, new_user.username)):
        return {'user': new_user, 'detail': 'Successfully created user but activation email was not sent!'}
    return {'user': new_user, 'detail': 'Successfully created'}


@router.post('/login', response_model=TokenModel, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = await repository_users.get_user_by_email(body.username, db)
    """
    Login for signed up user. Denies attempt if user not exist, email not confirmed, password not correct.

    :param body: The passed data for login.
    :type body: OAuth2PasswordRequestForm
    :param db:
    :type db: Session
    :rtype: JSON
    """    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Wrong user')
    if not user.confirmed:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed")
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Wrong password')
    
    access_token = await auth_service.create_access_token(data={'sub': user.email})
    refresh_token = await auth_service.create_refresh_token(data={'sub': user.email})
    await repository_users.update_token(user, refresh_token, db)
    return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'bearer'}

@router.get('/refresh_token', response_model=TokenModel, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    """
    Get new access token for user. Or null current refresh token in DB if the one that sent is outdated.

    :param credentials: Data for 'Authorization' header that includes 'Bearer' and the token.
    :type credentials: HTTPAuthorizationCredentials
    :param db:
    :type db: Session
    :rtype: JSON
    """    
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repository_users.update_token(user, None, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repository_users.update_token(user, refresh_token, db)
    return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'bearer'}


@router.post('/request_email', description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=2, seconds=60))])
async def request_email(body: RequestEmail, db: Session = Depends(get_db)):
    """
    Request for new verification email. Sends it or denies attempt if already confirmed.

    :param body: A class that contains .email (and possibly something else)
    :type body: RequestEmail
    :param db:
    :type db: Session
    :rtype: JSON
    """ 
    user = await repository_users.get_user_by_email(body.email, db)

    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        # background_tasks.add_task(send_verification, user.email, user.username)
        await send_verification(user.email, user.username)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Wrong user')
       
    return {"message": "Check your email for confirmation."}


@router.post('/reset_pwd', description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=2, seconds=60))])
async def reset_pwd(body: RequestEmail, db: Session = Depends(get_db)):
    """
    Sends an email with reset password. Denies if user does not exist. Requires email address.

    :param body: A class that contains .email of the user (and possibly something else)
    :type body: RequestEmail
    :param db:
    :type db: Session
    :rtype: JSON
    """ 
    user = await repository_users.get_user_by_email(body.email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Wrong user')
    
    email_token = await send_reset(user.email, user.username)
    await auth_service.reset_password(body.email, email_token, db)
    
    return {"message": "Check your email for new password."}