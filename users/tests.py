from django.test import TestCase
from .models import UserAccount
# Users Test Cases
# Create your tests here.

class UserAccountTest(TestCase):
    def testCanCreateAccount(self):
        ta = UserAccount(
            username="penguinrider",
            password="password123",
            email="asd@asd.com",
            first_name="penguin",
            last_name="rider",
            bio="Hi im a penguinrider",
            profile_picture="default.png"
            )
        ta.save()
        
        ta_from_db = UserAccount.objects.all().get(pk=ta.id)
        self.assertEquals(ta.username,ta_from_db.username)
        self.assertEquals(ta.password,ta_from_db.password)
        self.assertEquals(ta.email,ta_from_db.email)
        self.assertEquals(ta.first_name,ta_from_db.first_name)
        self.assertEquals(ta.last_name,ta_from_db.last_name)
        self.assertEquals(ta.bio,ta_from_db.bio)
        
    def testCanUpdateAccountDetails(self):
        ta = UserAccount(
            username="penguinrider",
            password="password123",
            email="asd@asd.com",
            first_name="penguin",
            last_name="rider",
            bio="Hi im a penguinrider",
            profile_picture="default.png"
            )
        ta.save()
        
        ta.username="penguinrider123"
        ta.password="password12345"
        ta.email="qwe@qwe.com"
        ta.save()
        
        ta_from_db = UserAccount.objects.all().get(pk=ta.id)
        self.assertEquals(ta_from_db.username,"penguinrider123")
        self.assertEquals(ta_from_db.password,"password12345")
        self.assertEquals(ta_from_db.email,"qwe@qwe.com")
        
    def testCanDeleteAccount(self):
        ta = UserAccount(
            username="penguinrider",
            password="password123",
            email="asd@asd.com",
            first_name="penguin",
            last_name="rider",
            bio="Hi im a penguinrider",
            profile_picture="default.png"
            )        
        ta.save()
        
        UserAccount.objects.filter(id=ta.id).delete()
        ta_from_db=list(UserAccount.objects.all().filter(pk=ta.id))
        self.assertEquals(ta_from_db,[])
        