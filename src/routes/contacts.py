from typing import List
from icecream import ic

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactModel
from src.repository import contacts as repository_contacts

from pydantic import ValidationError

router = APIRouter(prefix='/contacts', tags=['contacts'])

@router.get('/', response_model=List[ContactModel])
async def read_contacts(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(skip, limit, db)
    return contacts

@router.get('/bd', response_model=List[ContactModel])
async def check_birthdays(limit: int = 7, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_upcoming_birthdays(limit, db)
    return contacts

@router.get('/{fullname}', response_model=ContactModel)
async def read_contact(query: str, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(query, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact was not found')
    return contact

@router.post("/", response_model=ContactModel)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    try:
        return await repository_contacts.create_contact(body, db)
    except ValidationError as e:
        ic(e.errors)
        return {'detail': e.errors}

@router.put('/{fullname}', response_model=ContactModel)
async def update_contact(body: ContactModel, fullname: str, db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(fullname, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact was not found')
    return contact

@router.delete('/{fullname}', response_model=ContactModel)
async def remove_contact(fullname: str, db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(fullname, db)
    if contact is None:    
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact was not found')
    return contact