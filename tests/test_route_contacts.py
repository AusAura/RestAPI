from unittest.mock import MagicMock, patch, AsyncMock
from fastapi_limiter import FastAPILimiter

import pytest

from icecream import ic

from src.services.auth import auth_service
from src.database.models import User

# pytest tests/test_route_contacts.py -v

# from src.database.models import Contact

    # get_contacts,
    # get_contact,
    # get_upcoming_birthdays,
    # create_contact,
    # update_contact,
    # remove_contact,
    # update_avatar,

@pytest.fixture()
def token(client, user, session, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.services.email.send_verification", mock_send_email)
    client.post("/api/auth/signup", json=user)
    current_user: User = session.query(User).filter(User.email == ic(user.get('email'))).first()
    current_user.confirmed = True
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('email'), "password": user.get('password')},
    )
    data = response.json()
    return data["access_token"]


def test_create_contact(client, token, contact, monkeypatch):
    ic('showtime!')
    # with patch.object(auth_service, 'r') as r_mock:
    #     r_mock.get.return_value = None
    #     monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
    #     monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
    #     monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
    response = client.post(
            '/api/contacts/',
            json=contact,
            headers={'Authorization': f'Bearer {token}'}
        )

    assert response.status_code == 201, response.text
    data = response.json()
    assert data['fullname'] == 'testtest'


def test_get_contacts(client, token, user):
    # with patch.object(auth_service, 'r') as r_mock:
    #     r_mock.get.return_value = None
    #     monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
    #     monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
    #     monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
    response = client.get(
            '/api/contacts/',
            headers={'Authorization': f'Bearer {token}'}
            )
        
    assert response.status_code == 200, response.text
    data = ic(response.json())
    assert data[0]['user']['email'] == user.get('email')
        # assert 'id' in data['user']