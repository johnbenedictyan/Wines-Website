from django.test import TestCase
from .forms import ContactForm
# Website Test Cases
# Create your tests here.
class WebsiteURLTest(TestCase):
    def testCanLoadMainPage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
    
    def testCanLoadContactPage(self):
        response = self.client.get('/contact-us/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
    
    def testCanLoadAboutUsPage(self):
        response = self.client.get('/about-us/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about-us.html')
    
    def testCannotLoadNonExistentPage(self):
        response = self.client.get('/flyingpenguin')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

class WebsiteFormTest(TestCase):
    def testValidContactForm(self):
        test_form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': 12345678,
            'email_address': 'testuser@testuseremail.com',
            'message': 'Hi I would like to say that I am a test user.',
        }
        test_form = ContactForm(
            data=test_form_data
            )
        self.assertTrue(test_form.is_valid())
    
    def testMissingFirstNameErrorMessage(self):
        test_form_data = {
            'last_name': 'User',
            'phone_number': 12345678,
            'email_address': 'testuser@testuseremail.com',
            'message': 'Hi I would like to say that I am a test user.',
        }
        test_form = ContactForm(
            data=test_form_data
            )
        self.assertFalse(test_form.is_valid())
        response = self.client.post('/contact-us/', test_form_data)
        self.assertFormError(
            response,
            'contact_form',
            'first_name',
            'This field is required.'
            )
        
    def testMissingLastNameErrorMessage(self):
        test_form_data = {
            'first_name': 'Test',
            'phone_number': 12345678,
            'email_address': 'testuser@testuseremail.com',
            'message': 'Hi I would like to say that I am a test user.',
        }
        test_form = ContactForm(
            data=test_form_data
            )
        self.assertFalse(test_form.is_valid())
        response = self.client.post('/contact-us/', test_form_data)
        self.assertFormError(
            response,
            'contact_form',
            'last_name',
            'This field is required.'
            )
    
    def testMissingPhoneNumberErrorMessage(self):
        test_form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email_address': 'testuser@testuseremail.com',
            'message': 'Hi I would like to say that I am a test user.',
        }
        test_form = ContactForm(
            data=test_form_data
            )
        self.assertFalse(test_form.is_valid())
        response = self.client.post('/contact-us/', test_form_data)
        self.assertFormError(
            response,
            'contact_form',
            'phone_number',
            'This field is required.'
            )
    
    def testMissingEmailAddressErrorMessage(self):
        test_form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': 12345678,
            'message': 'Hi I would like to say that I am a test user.',
        }
        test_form = ContactForm(
            data=test_form_data
            )
        self.assertFalse(test_form.is_valid())
        response = self.client.post('/contact-us/', test_form_data)
        self.assertFormError(
            response,
            'contact_form',
            'email_address',
            'This field is required.'
            )
    
    def testMissingMessageErrorMessage(self):
        test_form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': 12345678,
            'email_address': 'testuser@testuseremail.com',
        }
        test_form = ContactForm(
            data=test_form_data
            )
        self.assertFalse(test_form.is_valid())
        response = self.client.post('/contact-us/', test_form_data)
        self.assertFormError(
            response,
            'contact_form',
            'message',
            'This field is required.'
            )
            
    def testInvalidPhoneNumberErrorMessage(self):
        test_form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': 'This is not a phone number.',
            'email_address': 'testuser@testuseremail.com',
            'message': 'Hi I would like to say that I am a test user.',
        }
        test_form = ContactForm(
            data=test_form_data
            )
        self.assertFalse(test_form.is_valid())
        response = self.client.post('/contact-us/', test_form_data)
        self.assertFormError(
            response,
            'contact_form',
            'phone_number',
            'Enter a whole number.'
            )
    
    def testInvalidEmailAddressErrorMessage(self):
        test_form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': 12345678,
            'email_address': 'This is not a valid email address.',
            'message': 'Hi I would like to say that I am a test user.',
        }
        test_form = ContactForm(
            data=test_form_data
            )
        self.assertFalse(test_form.is_valid())
        response = self.client.post('/contact-us/', test_form_data)
        self.assertFormError(
            response,
            'contact_form',
            'email_address',
            'Enter a valid email address.'
            ) 
    