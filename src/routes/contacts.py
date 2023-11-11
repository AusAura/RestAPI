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

from src.services.slowapi import limiter
from fastapi import Request

# from fastapi import Request
# from src.services.slowapi import limiter
# from main import contacts_router as router

router = APIRouter(prefix='/contacts', tags=['contacts'])

# @router.get('/', response_model=List[ContactModel], description='No more than 10 requests per minute',
#             dependencies=[Depends(RateLimiter(times=10, seconds=60))])
@router.get('/', response_model=List[ContactModel], description='No more than 10 requests per minute')
@limiter.limit("10/minute")
async def read_contacts(request: Request, skip: int = 0, limit: int = 20, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    Shows full list of contacts for user

    :param skip: 
    :type skip: int
    :param limit:
    :type limit: int
    :param user:
    :type user: User
    :param db:
    :type db: Session
    :rtype: List[Contact]
    """
    ic('I\'m fine until the function')
    contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)
    return contacts

# @router.get('/bd', response_model=List[ContactModel], description='No more than 10 requests per minute',
#             dependencies=[Depends(RateLimiter(times=10, seconds=60))])
@router.get('/bd', response_model=List[ContactModel], description='No more than 10 requests per minute')
@limiter.limit("10/minute")
async def check_birthdays(request: Request, days_range: int = 7, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    Checks the birthdays in the set range but only to the end of the year.

    :param days_range: A range in which bdays will be shown. If days_range > days left until the end of the year, it will search only until the end of it.
    :type skip: int
    :param user:
    :type user: User
    :param db:
    :type db: Session
    :rtype: List[Contact]
    """
    contacts = await repository_contacts.get_upcoming_birthdays(days_range, current_user, db)
    return contacts

# @router.get('/{query}', response_model=ContactModel, description='No more than 10 requests per minute',
#             dependencies=[Depends(RateLimiter(times=10, seconds=60))])
@router.get('/{query}', response_model=ContactModel, description='No more than 10 requests per minute')
@limiter.limit("10/minute")
async def read_contact(request: Request, query: str, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    Shows one contact for user

    :param query: A part of fullname or email address that is used for query to find the contact.
    :type query: str
    :param user:
    :type user: User
    :param db:
    :type db: Session
    :rtype: Contact
    """
    contact = await repository_contacts.get_contact(query, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact was not found')
    return contact

# @router.post("/", response_model=ContactModel, status_code=status.HTTP_201_CREATED, description='No more than 2 requests per minute',
#             dependencies=[Depends(RateLimiter(times=2, seconds=60))])
@router.post("/", response_model=ContactModel, status_code=status.HTTP_201_CREATED, description='No more than 2 requests per minute')
@limiter.limit("2/minute")
async def create_contact(request: Request, body: ContactModel, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    Creates a new contact.

    :param body: Data for contact.
    :type skip: ContactModel
    :param user:
    :type user: User
    :param db:
    :type db: Session
    :rtype: Contact
    """
    try:
        return await repository_contacts.create_contact(body, current_user, db)
    except ValidationError as e:
        ic(e.errors)
        return {'detail': e.errors}

# @router.put('/{contact_id}', response_model=ContactModel, description='No more than 10 requests per minute',
#             dependencies=[Depends(RateLimiter(times=10, seconds=60))])
@router.put('/{contact_id}', response_model=ContactModel, description='No more than 10 requests per minute')
@limiter.limit("10/minute")
async def update_contact(request: Request, body: ContactModel, contact_id: int, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    Updates the contact by contact_id. Returns None if contact with contact_id does not exist.

    :param contact_id: The ID of the contact.
    :type contact_id: int
    :param body: Data for the contact.
    :type limit: ContactModel
    :param user:
    :type user: User
    :param db:
    :type db: Session
    :rtype: Contact
    """
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact was not found')
    return contact

@router.patch('/{contact_id}/avatar', response_model=ContactModel)
@limiter.limit("10/minute")
async def update_avatar_contact(request: Request, contact_id, file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    """
    Updates the avatar URL for contact with contact_id. Returns None if contact with contact_id does not exist.

    :param contact_id: The ID of the contact.
    :type contact_id: int
    :param url: An URL for the avator on the cloud server..
    :type url: str
    :param db:
    :type db: Session
    :rtype: Contact | None
    """
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

# @router.delete('/{contact_id}', response_model=ContactModel, description='No more than 10 requests per minute',
#             dependencies=[Depends(RateLimiter(times=10, seconds=60))])
@router.delete('/{contact_id}', response_model=ContactModel, description='No more than 10 requests per minute')
@limiter.limit("10/minute")
async def remove_contact(request: Request, contact_id: int, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    Removes the contact by contact_id. Returns None if contact with contact_id does not exist.

    :param contact_id: The ID of the contact.
    :type contact_id: int
    :param user:
    :type user: User
    :param db:
    :type db: Session
    :rtype: Contact
    """
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:    
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact was not found')
    return contact