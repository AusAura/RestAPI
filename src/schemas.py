from datetime import datetime, date
from pydantic import BaseModel, Field

class ContactModel(BaseModel):
    fullname: str = Field(max_length=150)
    email: str = Field(max_length=200)
    phone_number: int
    birthday: date
    additional: str = Field(max_length=500)

    class Config:
        orm_mode = True