from sqlalchemy import Column, Integer, String, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String(150), nullable=False, unique=True)
    email = Column(String(200), nullable=True)
    phone_number = Column(Integer, nullable=True)
    birthday = Column(Date, nullable=True)
    additional = Column(String(500), nullable=True)
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref='contacts')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(250), nullable=False)
    created_at = Column('created_at', DateTime, default=func.now())
    refresh_token = Column(String(255), nullable=True)