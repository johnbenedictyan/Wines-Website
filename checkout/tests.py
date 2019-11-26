from django.test import TestCase
from users.models import UserAccount
from products.models import Product
# Checkout Test Cases
# Create your tests here.
DEFAULT_IMAGE_UUID = "0662e7f0-e44d-4f4b-8482-715f396f5fb0"

def create_account():
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
    return ta

def create_test_product(seller_id):
    tp = Product(
            name="Generic Wine",
            year=2013,
            description="This is a bottle of Generic Wine",
            price=53.99,
            quantity_in_stock=100,
            product_picture=DEFAULT_IMAGE_UUID,
            region="FRANCE",
            nodes="Fruits",
            body="Light",
            seller_id=seller_id,
            views=0
            )
    tp.save()
    return tp
    
class CheckoutUrlGeneralTest(TestCase):
    def setUp(self):
        ta = create_account()
        ta.set_password('password123')
        ta.save()
        ta_2 = UserAccount(
            username="penguinrider2",
            password="password123",
            email="a@a.com",
            first_name="penguin",
            last_name="rider",
            bio="Hi im a penguinrider",
            profile_picture=DEFAULT_IMAGE_UUID
            )
        ta_2.set_password('password123')
        ta_2.save()
        create_test_product(ta.id)
        
    def testCanLoadViewCartPageWithLogin(self):
        self.client.login(
            username='penguinrider',
            password='password123'
            )
        response = self.client.get('/checkout/cart/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart.html') 
    
    def testCannotLoadViewCartPageWithoutLogin(self):
        response = self.client.get('/checkout/cart/')
        self.assertRedirects(
            response,
            '/users/log-in/?next=/checkout/cart/',
            status_code=302,
            target_status_code=200
            ) 