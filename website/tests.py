from django.test import TestCase
from django.contrib import auth
from .forms import ContactForm,BlogCreatorFrom
from .models import Contact,Blog
from users.models import UserAccount
# Website Test Cases
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
    
def create_test_blog(ta):
    tb = Blog(
        headline="asd",
        body="zxc",
        writer=ta.username,
        )
    tb.save()
    return tb
        
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
        response = self.client.post('/contact-us/', test_form_data)
        self.assertRedirects(
            response,
            '/',
            status_code=302,
            target_status_code=200
            )
        contact_from_db = Contact.objects.get(pk=1)
        self.assertEqual(
            contact_from_db.first_name,
            test_form_data['first_name']
            )
        self.assertEqual(
            contact_from_db.last_name,
            test_form_data['last_name']
            )
        self.assertEqual(
            contact_from_db.phone_number,
            test_form_data['phone_number']
            )
        self.assertEqual(
            contact_from_db.email_address,
            test_form_data['email_address']
            )
        self.assertEqual(
            contact_from_db.message,
            test_form_data['message']
            )
    
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
    
class BlogTest(TestCase):
    def testCanCreateBlog(self):
        ta = create_test_account()
        tb = create_test_blog(ta)
        
        tb_from_db = Blog.objects.all().get(pk=tb.id)
        self.assertEquals(
            tb.headline,
            tb_from_db.headline
            )
        self.assertEquals(tb.body,tb_from_db.body)
        self.assertEquals(tb.writer,ta.username)
        
class BlogUrlGeneralTest(TestCase):
    def setUp(self):
        create_test_blog(create_test_account())
        
    def testCanBloghubPage(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bloghub.html')
    
    def testCanLoadBlogSinglePage(self):
        response = self.client.get('/blog/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog.html')
        
    def testCannotLoadNonExistentBlogSinglePage(self):
        response = self.client.get('/blog/999/')
        self.assertRedirects(
            response,
            '/blog/',
            status_code=302,
            target_status_code=200
            )
        
class BlogUrlCreationTest(TestCase):
    def setUp(self):
        create_test_blog(create_test_account())
        
    def testCanLoadBlogCreationPage(self):
        self.client.login(
            username='penguinrider',
            password='password123'
            )
        response = self.client.get('/blog/create/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog-creator.html')
        
    def testCannotLoadBlogCreationPageWithoutLogin(self):
        response = self.client.get('/blog/create/')
        self.assertRedirects(
            response,
            '/users/log-in/?next=/blog/create/',
            status_code=302,
            target_status_code=200
            )
            
class BlogFormCreationTest(TestCase):
    def setUp(self):
        create_test_account()
        self.client.login(
            username='penguinrider',
            password='password123'
            )
        
    def testValidBlogCreatorFromCreationSubmission(self):
        user = auth.get_user(self.client)
        test_form_data = {
            'headline':"Generic Headline",
            'body':"Generic Body",
            'writer':user.username,
        }
        test_form = BlogCreatorFrom(
            data=test_form_data
            )
        
        self.assertTrue(test_form.is_valid())
        response = self.client.post('/blog/create/', test_form_data)
        self.assertRedirects(
            response,
            '/blog/',
            status_code=302,
            target_status_code=200
            )
        
    def testMissingHeadlineErrorMessage(self):
        user = auth.get_user(self.client)
        test_form_data = {
            'body':"Generic Body",
            'writer':user.username,
        }
        test_form = BlogCreatorFrom(
            data=test_form_data
            )
        self.assertFalse(test_form.is_valid())
        response = self.client.post('/blog/create/', test_form_data)
        self.assertFormError(
            response,
            'blog_form',
            'headline',
            'This field is required.'
            )
        
    def testMissingBodyErrorMessage(self):
        user = auth.get_user(self.client)
        test_form_data = {
            'headline':"Generic Headline",
            'writer':user.username,
        }
        test_form = BlogCreatorFrom(
            data=test_form_data
            )
        self.assertFalse(test_form.is_valid())
        response = self.client.post('/blog/create/', test_form_data)
        self.assertFormError(
            response,
            'blog_form',
            'body',
            'This field is required.'
            )