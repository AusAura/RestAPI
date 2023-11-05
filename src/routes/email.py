from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.repository import users as repository_users
from src.services.auth import auth_service
from fastapi_limiter.depends import RateLimiter

router = APIRouter(prefix='/email', tags=['email'])

@router.get("/confirm/{email_token}", description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def confirmed_email(email_token: str, db: Session = Depends(get_db)):
    email = await auth_service.get_email_from_token(email_token)
    user = await repository_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    
    await repository_users.confirmed_email(email, db)
    return {"message": "Email confirmed"}