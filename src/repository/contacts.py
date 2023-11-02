from icecream import ic

from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from src.database.models import Contact, User
from src.schemas import ContactModel

from datetime import datetime, timedelta, date

async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()

async def get_contact(query: str, user: User, db: Session) -> Contact:
    result = db.query(Contact).filter(and_(Contact.fullname.like(f"%{query}%"), Contact.user_id == user.id)).first()
    if result:
        return result
    result = db.query(Contact).filter(and_(Contact.email.like(f"%{query}%"), Contact.user_id == user.id)).first()
    return result

async def get_upcoming_birthdays(days_range: int, user: User, db: Session) -> List[Contact]:
    today = ic(datetime.now().date())
    end_of_year = datetime(today.year, 12, 31).date()
    days_left = ic((end_of_year - today).days)

    if days_range > days_left:
        days_range = days_left

    end = ic(today + timedelta(days=days_range))
    
    today_date = ic(today.strftime('%m-%d'))
    end_date = ic(end.strftime('%m-%d'))

    upcoming_birthdays = db.query(Contact).filter(Contact.user_id == user.id).filter(func.to_char(Contact.birthday, 'MM-DD').between(today_date, end_date)).all()
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

async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    contact = Contact(fullname=body.fullname,
                    email= body.email,
                    phone_number=body.phone_number,
                    birthday = body.birthday,
                    additional = body.additional,
                    user_id = user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

async def update_contact(contact_id: int, body: ContactModel, user: User, db: Session) -> Contact | None:
    # contact = db.query(Contact).filter(Contact.fullname.like(f"%{fullname}%")).first()
    contact = db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.id == contact_id)).first()
    if contact:
        contact.fullname=body.fullname
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        contact.additional = body.additional
        db.commit()
    return contact

async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    # contact = db.query(Contact).filter(Contact.fullname.like(f"%{fullname}%")).first()
    contact = db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.id == contact_id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
