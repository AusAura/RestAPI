from unittest.mock import MagicMock, patch
import pytest

from icecream import ic

from src.services.auth import auth_service
from src.database.models import User

## pytest tests/test_route_contacts.py -v -s

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


def test_create_contact(client, token, contact):
    ic('showtime!')
    response = client.post(
            '/api/contacts/',
            json=contact,
            headers={'Authorization': f'Bearer {token}'}
        )

    assert response.status_code == 201, response.text
    data = response.json()
    assert data['fullname'] == 'testtest'

def test_get_contacts(client, token, contact):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
    
        response = client.get(
                    '/api/contacts/',
                    headers={'Authorization': f'Bearer {token}'}
                    )
        
    assert response.status_code == 200, response.text
    data = ic(response.json())
    data = data[0]
    assert data.get('email') == contact.get('email')
    assert 'user_id' in data


def test_get_contact(client, token, contact):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None

        response = client.get(
                        '/api/contacts/test',
                        headers={'Authorization': f'Bearer {token}'}
                        )
        
    assert response.status_code == 200, response.text
    data = ic(response.json())
    assert data.get('email') == contact.get('email')
    assert 'user_id' in data


### Not functional due to using SQLite instead of Postgres during tests
# def test_check_birthdays(client, token, contact):
#     with patch.object(auth_service, 'r') as r_mock:
#         r_mock.get.return_value = None
#         response = client.get(
#                         '/api/contacts/bd',
#                         headers={'Authorization': f'Bearer {token}'}
#                         ) 

#     assert response.status_code == 200, response.text
#     data = data[0]
#     assert data.get('email') == contact.get('email')


def test_update_contact(client, token, contact_2):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None

        response = client.put(
                        '/api/contacts/1',
                        json=contact_2,
                        headers={'Authorization': f'Bearer {token}'}
                        )
        
    assert response.status_code == 200, response.text
    data = ic(response.json())
    assert data.get('email') == contact_2.get('email')
    assert 'user_id' in data


def test_update_contact(client, token, contact_2):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None

        response = client.put(
                        '/api/contacts/1',
                        json=contact_2,
                        headers={'Authorization': f'Bearer {token}'}
                        )
        
    assert response.status_code == 200, response.text
    data = ic(response.json())
    assert data.get('email') == contact_2.get('email')
    assert 'user_id' in data


def test_update_avatar_contact(client, token, contact_2):
    file_data = {"file": ("your_file_content_here", "filename.ext")}  # Замените на данные вашего файла
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None

        with patch('src.routes.contacts.cloudinary.uploader.upload', return_value={'version': 'example_version'}):
            with patch('src.routes.contacts.cloudinary.CloudinaryImage.build_url', return_value='example_url'):

                response = client.patch(
                        '/api/contacts/1/avatar',
                        files=file_data,
                        headers={'Authorization': f'Bearer {token}'}
                        )
        
    assert response.status_code == 200, response.text
    data = ic(response.json())
    assert data.get('email') == contact_2.get('email')
    assert 'user_id' in data

def test_remove_contact(client, token, contact_2):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None

        response = client.delete(
                        '/api/contacts/1',
                        headers={'Authorization': f'Bearer {token}'}
                        )
        
    assert response.status_code == 200, response.text
    data = ic(response.json())
    assert data.get('email') == contact_2.get('email')
    assert 'user_id' in data
    
# pytest tests/test_route_contacts.py -v -s