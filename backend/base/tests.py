from django.test import TestCase
import datetime
from .models import Organisation, User
from uuid import uuid4 

# Create your tests here.


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(email="example@email.com",
                            username='example')
    
    def test_user(self):
        john = User.objects.get(username="example")
        self.assertEqual(type(john.id), type(uuid4()))
        self.assertEqual(john.email, "example@email.com")
        self.assertEqual(john.username, "example")
    
    
class OrganisationTestCase(TestCase):
    def setUp(self):
        john = User.objects.create(email="johndoe@email.com",
                            username='johndoe')
        org = Organisation.objects.create(
            owner=john,
            name="GFSC",
            address="19, Adeyemi street",
            email="gfsc@email.com",
        )
    def test_organisation(self):
        org = Organisation.objects.get(name="GFSC")
        john = User.objects.get(id=org.owner.id)
        self.assertEqual(org.owner, john)
        self.assertEqual(org.name, "GFSC")
        self.assertEqual(org.address, "19, Adeyemi street")
        self.assertEqual(org.email, "gfsc@email.com")
        self.assertEqual(org.telephone, None)
        self.assertEqual(type(org.created), datetime.datetime)
        self.assertEqual(type(org.updated), datetime.datetime)
