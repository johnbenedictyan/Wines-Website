from django.test import TestCase
from .models import UserAccount
from .forms import RegisterForm
from django.contrib import auth

# Users Test Cases
# Create your tests here.
DEFAULT_IMAGE_UUID = "0662e7f0-e44d-4f4b-8482-715f396f5fb0"


def create_test_account():
    ta = UserAccount(
        username="penguinrider",
        password="password123",
        email="asd@asd.com",
        first_name="penguin",
        last_name="rider",
        bio="Hi im a penguinrider",
        profile_picture=DEFAULT_IMAGE_UUID
    )
    ta.set_password('password123')
    ta.save()
    return ta


class UserAccountTest(TestCase):
    def testCanCreateAccount(self):
        ta = UserAccount(
            username="penguinrider",
            password="password123",
            email="asd@asd.com",
            first_name="penguin",
            last_name="rider",
            bio="Hi im a penguinrider",
            profile_picture=DEFAULT_IMAGE_UUID
        )
        ta.save()

        ta_from_db = UserAccount.objects.all().get(pk=ta.id)
        self.assertEquals(ta.username, ta_from_db.username)
        self.assertEquals(ta.password, ta_from_db.password)
        self.assertEquals(ta.email, ta_from_db.email)
        self.assertEquals(ta.first_name, ta_from_db.first_name)
        self.assertEquals(ta.last_name, ta_from_db.last_name)
        self.assertEquals(ta.bio, ta_from_db.bio)

    def testCanUpdateAccountDetails(self):
        ta = create_test_account()

        ta.username = "penguinrider123"
        ta.password = "password12345"
        ta.email = "qwe@qwe.com"
        ta.save()

        ta_from_db = UserAccount.objects.all().get(pk=ta.id)
        self.assertEquals(ta_from_db.username, "penguinrider123")
        self.assertEquals(ta_from_db.password, "password12345")
        self.assertEquals(ta_from_db.email, "qwe@qwe.com")

    def testCanDeleteAccount(self):
        ta = create_test_account()

        UserAccount.objects.filter(id=ta.id).delete()
        ta_from_db = list(UserAccount.objects.all().filter(pk=ta.id))
        self.assertEquals(ta_from_db, [])


class UserAccountUrlTest(TestCase):
    def setUp(self):
        create_test_account()

    def testCanRedirectToLoginUrlForLoginRequiredPages(self):
        response = self.client.get('/users/')
        self.assertRedirects(
            response,
            '/users/log-in/?next=/users/',
            status_code=302,
            target_status_code=200
        )

    def testCanLoadLoginPage(self):
        response = self.client.get('/users/log-in/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def testCanLoadRegisterPage(self):
        response = self.client.get('/users/registration/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def testCanLoadAccountPage(self):
        self.client.login(username='penguinrider', password='password123')
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account.html')

    def testCanLogout(self):
        self.client.login(
            username='penguinrider',
            password='password123'
        )
        response = self.client.get('/users/log-out/')
        self.assertRedirects(
            response,
            '/',
            status_code=302,
            target_status_code=200
        )


class UserAccountLoginFormTest(TestCase):
    def setUp(self):
        create_test_account()

    def testValidLogin(self):
        test_form_data = {
            'username': 'penguinrider',
            'password': 'password123',
        }
        response = self.client.post(
            '/users/log-in/',
            test_form_data
        )
        self.assertRedirects(
            response,
            '/',
            status_code=302,
            target_status_code=200
        )
        self.assertIn('_auth_user_id', self.client.session)

    def testInvalidLogin(self):
        test_form_data = {
            'username': 'penguinrider',
            'password': 'password1234',
        }
        response = self.client.post(
            '/users/log-in/',
            test_form_data
        )
        self.assertRedirects(
            response,
            '/users/log-in/',
            status_code=302,
            target_status_code=200
        )
        self.assertNotIn('_auth_user_id', self.client.session)


class UserAccountRegisterFormTest(TestCase):
    def ValidRegisterFormSubmission(self):
        test_form_data = {
            'username': 'johndoe',
            'first_name': 'john',
            'last_name': 'doe',
            'email': 'johndoe@johndoe.com',
            'password1': 'Password123!',
            'password2': 'Password123!',
            'profile_picture': DEFAULT_IMAGE_UUID
        }

        test_form = RegisterForm(
            data=test_form_data
        )

        self.assertTrue(test_form.is_valid())

    def testMissingUserNameErrorMessage(self):
        test_form_data = {
            'first_name': 'john',
            'last_name': 'doe',
            'email': 'johndoe@johndoe.com',
            'password1': 'Password123!',
            'password2': 'Password123!',
            'profile_picture': DEFAULT_IMAGE_UUID
        }

        test_form = RegisterForm(
            data=test_form_data
        )
        self.assertFalse(test_form.is_valid())
        response = self.client.post('/users/registration/', test_form_data)
        self.assertFormError(
            response,
            'registration_form',
            'username',
            'This field is required.'
        )

    def testMissingFirstNameErrorMessage(self):
        test_form_data = {
            'username': 'johndoe',
            'last_name': 'doe',
            'email': 'johndoe@johndoe.com',
            'password1': 'Password123!',
            'password2': 'Password123!',
            'profile_picture': DEFAULT_IMAGE_UUID
        }

        test_form = RegisterForm(
            data=test_form_data
        )
        self.assertFalse(test_form.is_valid())
        response = self.client.post('/users/registration/', test_form_data)
        self.assertFormError(
            response,
            'registration_form',
            'first_name',
            'This field is required.'
        )

    def testMissingLastNameErrorMessage(self):
        test_form_data = {
            'username': 'johndoe',
            'first_name': 'john',
            'email': 'johndoe@johndoe.com',
            'password1': 'Password123!',
            'password2': 'Password123!',
            'profile_picture': DEFAULT_IMAGE_UUID
        }

        test_form = RegisterForm(
            data=test_form_data
        )
        self.assertFalse(test_form.is_valid())
        response = self.client.post('/users/registration/', test_form_data)
        self.assertFormError(
            response,
            'registration_form',
            'last_name',
            'This field is required.'
        )

    def testMissingEmailErrorMessage(self):
        test_form_data = {
            'username': 'johndoe',
            'first_name': 'john',
            'last_name': 'doe',
            'password1': 'Password123!',
            'password2': 'Password123!',
            'profile_picture': DEFAULT_IMAGE_UUID
        }

        test_form = RegisterForm(
            data=test_form_data
        )
        self.assertFalse(test_form.is_valid())
        response = self.client.post('/users/registration/', test_form_data)
        self.assertFormError(
            response,
            'registration_form',
            'email',
            'This field is required.'
        )

    def testMissingPassword1ErrorMessage(self):
        test_form_data = {
            'username': 'johndoe',
            'first_name': 'john',
            'last_name': 'doe',
            'email': 'johndoe@johndoe.com',
            'password2': 'Password123!',
            'profile_picture': DEFAULT_IMAGE_UUID
        }

        test_form = RegisterForm(
            data=test_form_data
        )
        self.assertFalse(test_form.is_valid())
        response = self.client.post('/users/registration/', test_form_data)
        self.assertFormError(
            response,
            'registration_form',
            'password1',
            'This field is required.'
        )

    def testMissingPassword2ErrorMessage(self):
        test_form_data = {
            'username': 'johndoe',
            'first_name': 'john',
            'last_name': 'doe',
            'email': 'johndoe@johndoe.com',
            'password1': 'Password123!',
            'profile_picture': DEFAULT_IMAGE_UUID
        }

        test_form = RegisterForm(
            data=test_form_data
        )
        self.assertFalse(test_form.is_valid())
        response = self.client.post('/users/registration/', test_form_data)
        self.assertFormError(
            response,
            'registration_form',
            'password2',
            'This field is required.'
        )
