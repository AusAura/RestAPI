import unittest
from datetime import date
from unittest.mock import MagicMock

from icecream import ic

from sqlalchemy.orm import Session

# python -m unittest tests.test_unit_repository_users

from src.database.models import User
from src.schemas import UserModel
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,
)

class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_user_by_email_true(self):
        user = User()
        self.session.query().filter().first.return_value = user
        result = await get_user_by_email(email='test', db=self.session)
        self.assertEqual(result, user)

    async def test_get_user_by_email_false(self):
        self.session.query().filter().first.return_value = None
        result = await get_user_by_email(email='test', db=self.session)
        self.assertIsNone(result)

    async def test_create_user(self):
        user = UserModel(username='test12', password='testtest', email='test')
        self.session.commit.return_value = None
        result = await create_user(body=user, db=self.session)
        self.assertTrue(hasattr(result, "id"))
        self.assertEqual(result.username, user.username)
        self.assertEqual(result.password, user.password)
        self.assertEqual(result.email, user.email)

    async def test_update_token(self):
        token = 'test123'
        self.session.commit.return_value = None
        result = await update_token(user=self.user, token=token, db=self.session)
        self.assertEqual(result, self.user)

    async def test_confirmed_email(self):
        email = 'test@email.com'
        self.session.commit.return_value = None
        self.session.query().filter().first.return_value = self.user
        result = await confirmed_email(email=email, db=self.session)
        self.assertEqual(result, self.user)

if __name__ == '__main__':
    unittest.main()