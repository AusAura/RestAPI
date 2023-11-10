from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel

from icecream import ic

async def get_user_by_email(email: str, db: Session) -> User:
    """
    Returns user that have that email. Empty if fails.

    :param email: The email of the user.
    :type email: str
    :param db:
    :type db: Session
    :rtype: User | []
    """
    return db.query(User).filter(User.email == email).first()

async def create_user(body: UserModel, db: Session) -> User:
    """
    Creates the user with the passed data. Empty if fails.

    :param body: The passed data.
    :type body: UserModel
    :param db:
    :type db: Session
    :rtype: User | []
    """
    new_user = User(**body.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

async def update_token(user: User, token: str | None, db: Session) -> User:
    """
    Refresh token for the user.

    :param user: The user.
    :type user: User
    :param token: The passed token value.
    :type token: str
    :param db:
    :type db: Session
    :rtype: User
    """
    user.refresh_token = token
    db.commit()
    return user

async def confirmed_email(email: str, db: Session) -> User:
    """
    Confirms email for the user. Empty if not found.

    :param token: User email that should be confirmed.
    :type email: str
    :param db:
    :type db: Session
    :rtype: User | []
    """
    user = await get_user_by_email(email, db)
    if user:
        user.confirmed = True
        db.commit()
    return user
    