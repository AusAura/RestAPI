from typing import List
from icecream import ic

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.services.auth import auth_service
from src.schemas import ContactModel
from src.database.models import User
from src.repository import contacts as repository_contacts

from pydantic import ValidationError

router = APIRouter(prefix='/contacts', tags=['contacts'])

@router.get('/', response_model=List[ContactModel])
async def read_contacts(skip: int = 0, limit: int = 20, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)
    return contacts

@router.get('/bd', response_model=List[ContactModel])
async def check_birthdays(days_range: int = 7, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_upcoming_birthdays(days_range, current_user, db)
    return contacts

@router.get('/{query}', response_model=ContactModel)
async def read_contact(query: str, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(query, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact was not found')
    return contact

@router.post("/", response_model=ContactModel, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    try:
        return await repository_contacts.create_contact(body, current_user, db)
    except ValidationError as e:
        ic(e.errors)
        return {'detail': e.errors}

@router.put('/{contact_id}', response_model=ContactModel)
async def update_contact(body: ContactModel, contact_id: int, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact was not found')
    return contact

@router.delete('/{contact_id}', response_model=ContactModel)
async def remove_contact(contact_id: int, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:    
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact was not found')
    return contact