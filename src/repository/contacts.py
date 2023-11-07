from icecream import ic

from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from src.database.models import Contact, User
from src.schemas import ContactModel

from datetime import datetime, timedelta, date

async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
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

    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()

async def get_contact(query: str, user: User, db: Session) -> Contact:
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
    result = db.query(Contact).filter(and_(Contact.fullname.like(f"%{query}%"), Contact.user_id == user.id)).first()
    if result:
        return result
    result = db.query(Contact).filter(and_(Contact.email.like(f"%{query}%"), Contact.user_id == user.id)).first()
    return result

async def get_upcoming_birthdays(days_range: int, user: User, db: Session) -> List[Contact]:
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
    contact = Contact(fullname=body.fullname,
                    email= body.email,
                    phone_number=body.phone_number,
                    birthday = body.birthday,
                    additional = body.additional,
                    user_id = user.id,
                    avatar = body.avatar)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

async def update_contact(contact_id: int, body: ContactModel, user: User, db: Session) -> Contact | None:
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
    :rtype: Contact | None
    """
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
    """
    Removes the contact by contact_id. Returns None if contact with contact_id does not exist.

    :param contact_id: The ID of the contact.
    :type contact_id: int
    :param user:
    :type user: User
    :param db:
    :type db: Session
    :rtype: Contact | None
    """
    # contact = db.query(Contact).filter(Contact.fullname.like(f"%{fullname}%")).first()
    contact = db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.id == contact_id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_avatar(contact_id: int, url: str, db: Session) -> Contact | None:
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
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.avatar = url
        db.commit()
    return contact