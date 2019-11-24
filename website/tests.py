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