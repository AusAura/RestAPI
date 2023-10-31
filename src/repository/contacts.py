from typing import List
from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel

from datetime import datetime, timedelta, date

async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()

async def get_contact(query: str, db: Session) -> Contact:
    result = db.query(Contact).filter(Contact.fullname.like(f"%{query}%")).first()
    if result:
        return result
    result = db.query(Contact).filter(Contact.email.like(f"%{query}%")).first()
    return result

async def get_upcoming_birthdays(days_range: int, db: Session) -> List[Contact]:
    today = datetime.now().date()
    range = today + timedelta(days=days_range)
    upcoming_birthdays = db.query(Contact).filter(Contact.birthday.between(today, range)).all()
    return upcoming_birthdays

# async def get_upcoming_birthdays(limit: int, db: Session) -> List[Contact]:
#     today = datetime.now().date()
#     upcoming_birthdays = db.query(Contact).all()
#     upcoming_birthdays = sorted(
#         upcoming_birthdays,
#         key=lambda contact: (
#             (contact.birthday.month, contact.birthday.day) 
#             if (contact.birthday.month, contact.birthday.day) >= (today.month, today.day) 
#             else (contact.birthday.month + 12, contact.birthday.day)
#         )
#     )
#     return upcoming_birthdays[:limit]

async def create_contact(body: ContactModel, db: Session) -> Contact:
    contact = Contact(fullname=body.fullname,
                    email= body.email,
                    phone_number=body.phone_number,
                    birthday = body.birthday,
                    additional = body.additional)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

async def update_contact(contact_id: int, body: ContactModel, db: Session) -> Contact | None:
    # contact = db.query(Contact).filter(Contact.fullname.like(f"%{fullname}%")).first()
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.fullname=body.fullname
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        contact.additional = body.additional
        db.commit()
    return contact

async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    # contact = db.query(Contact).filter(Contact.fullname.like(f"%{fullname}%")).first()
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
