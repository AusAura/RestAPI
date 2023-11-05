from typing import List
from icecream import ic

from src.conf.config import settings

import cloudinary
import cloudinary.uploader

from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.services.auth import auth_service
from src.schemas import ContactModel
from src.database.models import User
from src.repository import contacts as repository_contacts
# from src.repository import users as repository_users

from pydantic import ValidationError
from fastapi_limiter.depends import RateLimiter

router = APIRouter(prefix='/contacts', tags=['contacts'])

@router.get('/', response_model=List[ContactModel], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contacts(skip: int = 0, limit: int = 20, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)
    return contacts

@router.get('/bd', response_model=List[ContactModel], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def check_birthdays(days_range: int = 7, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_upcoming_birthdays(days_range, current_user, db)
    return contacts

@router.get('/{query}', response_model=ContactModel, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contact(query: str, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(query, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact was not found')
    return contact

@router.post("/", response_model=ContactModel, status_code=status.HTTP_201_CREATED, description='No more than 2 requests per minute',
            dependencies=[Depends(RateLimiter(times=2, seconds=60))])
async def create_contact(body: ContactModel, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    try:
        return await repository_contacts.create_contact(body, current_user, db)
    except ValidationError as e:
        ic(e.errors)
        return {'detail': e.errors}

@router.put('/{contact_id}', response_model=ContactModel, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_contact(body: ContactModel, contact_id: int, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact was not found')
    return contact

@router.patch('/{contact_id}/avatar')
async def update_avatar_contact(contact_id, file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )

    r = cloudinary.uploader.upload(file.file, public_id=f'Contact_sss/{current_user.username}/{contact_id}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'Contact_sss/{current_user.username}/{contact_id}')\
                        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    contact = await repository_contacts.update_avatar(contact_id, src_url, db)
    return contact

@router.delete('/{contact_id}', response_model=ContactModel, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def remove_contact(contact_id: int, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:    
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact was not found')
    return contact