import pytest, redis
from datetime import date
from unittest.mock import patch, MagicMock

from icecream import ic

from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from src.database.models import Base
from src.database.db import get_db
from src.services.auth import auth_service

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# @pytest.fixture(scope="session", autouse=True)
# def initialize_fastapi_limiter():
#     ic('started mock redis')

#     def override_dependency(q: str | None = None):
#         return {"q": q, "skip": 5, "limit": 10}
    
#     app.dependency_overrides[RateLimiter] = override_dependency
      
#     r_mock = MagicMock(spec=redis.Redis)
#     FastAPILimiter.init(r_mock)

  
@pytest.fixture(scope='module')
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope='module')
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture(scope='module')
def user():
    return {"username": "deadpool", "email": "deadpool@example.com", "password": "123456789"}

    # fullname: str = Field(max_length=150)
    # email: str = Field(max_length=200)
    # phone_number: int
    # birthday: date
    # additional: str = Field(max_length=500)
    # user_id: int
    # avatar: str

@pytest.fixture(scope='module')
def contact():
    return {'fullname': 'testtest',
            'email': 'test@mail.com',
            'phone_number': 0,
            'birthday': str(date(year=2022, month=2, day=13)),
            'additional': 'test',
            'user_id': 1,
            'avatar': 'test-url'
    }

@pytest.fixture(scope='module')
def contact_2():
    return {'fullname': 'somenewtest',
            'email': 'newtest@mail.com',
            'phone_number': 1,
            'birthday': str(date(year=2022, month=2, day=13)),
            'additional': 'newtest',
            'user_id': 1,
            'avatar': 'newtest-url'
    }

