import unittest
from datetime import date
from unittest.mock import MagicMock

from icecream import ic

from sqlalchemy.orm import Session

# python -m unittest tests.test_unit_repository_contacts

from src.database.models import Contact, User
from src.schemas import ContactModel
from src.repository.contacts import (
    get_contacts,
    get_contact,
    get_upcoming_birthdays,
    create_contact,
    update_contact,
    remove_contact,
    update_avatar,
)

class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_true(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(query=contact.fullname, user=self.user, db=self.session)
        self.assertEqual(result, contact)
    
    async def test_get_contact_false(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(query='Jones', user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_contact(self):
        body = ContactModel(fullname='test', email='test', phone_number=0, birthday=date(year=2022, month=2, day=13), additional='test', user_id=1, avatar='None')
        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.fullname, body.fullname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone_number, body.phone_number)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.additional, body.additional)
        self.assertEqual(result.user_id, body.user_id)
        self.assertEqual(result.avatar, body.avatar)
        self.assertTrue(hasattr(result, "id"))

    async def test_update_contact_true(self):
        body = ContactModel(fullname='test', email='test', phone_number=0, birthday=date(year=2022, month=2, day=13), additional='test', user_id=1, avatar='None')
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(ic(result), ic(contact))

    async def test_remove_contact_true(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_false(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)
        
    async def test_update_contact_false(self):
        body = ContactModel(fullname='test', email='test', phone_number=0, birthday=date(year=2022, month=2, day=13), additional='test', user_id=1, avatar='None')
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_get_upcoming_birthdays(self):
        contacts = [Contact(), Contact()]
        self.session.query().filter.return_value.filter.return_value.all.return_value = contacts
        result = await get_upcoming_birthdays(days_range=7, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_update_avatar(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update_avatar(contact_id=1, url='https://test.com/contact/1', db=self.session)
        self.assertEqual(result, contact)

    
if __name__ == '__main__':
    unittest.main()