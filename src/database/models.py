from sqlalchemy import Column, Integer, String
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
