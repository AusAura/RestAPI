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


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    password: str = Field(min_length=6, max_length=10)
    email: str


class UserDB(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    
    class Config:
        orm_mode = True


class UserResponce(BaseModel):
    user: UserDB
    detail: str = 'Successfully created'


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'