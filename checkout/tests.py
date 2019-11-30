from django.test import TestCase
from users.models import UserAccount
from products.models import Product
from .models import Coupon
from datetime import timedelta,datetime
from .forms import CustomerDetailForm
from django.contrib import auth
# Checkout Test Cases
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
    
def create_test_coupon():
    tc = Coupon(
        coupon_code = 'testcoupon',
        )
    tc.save()
    return tc
    
class CheckoutUrlGeneralTest(TestCase):
    def setUp(self):
        ta = create_test_account()
        ta.set_password('password123')
        ta.save()
        
    def testCanLoadOrdersPageWithLogin(self):
        self.client.login(
            username='penguinrider',
            password='password123'
            )
        response = self.client.get('/checkout/orders/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders.html') 
    
    def testCannotLoadOrdersPageWithoutLogin(self):
        response = self.client.get('/checkout/orders/')
        self.assertRedirects(
            response,
            '/users/log-in/?next=/checkout/orders/',
            status_code=302,
            target_status_code=200
            ) 
    
class CheckoutCartViewFunctionTest(TestCase):
    def setUp(self):
        ta = create_test_account()
        ta.set_password('password123')
        ta.save()
        
    def testCanLoadViewCartPage(self):
        response = self.client.get('/checkout/cart/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart.html')

class CheckoutCartAddFunctionTest(TestCase):
    def setUp(self):
        ta = create_test_account()
        ta.set_password('password123')
        ta.save()
        create_test_product(ta.id)
        
    def testCanAddItemToCart(self):
        tp = Product.objects.get(pk=1)
        response = self.client.get('/checkout/cart/add/1/2/')
        self.assertRedirects(
            response,
            '/checkout/cart/',
            status_code=302,
            target_status_code=200
            )    
        user_cart = self.client.session['user_cart']
        self.assertEqual(len(user_cart['cart_items']), 1)
        self.assertEqual(user_cart['cart_items'][0]['product_number'], 1)
        self.assertEqual(user_cart['cart_items'][0]['quantity'], 2)
        self.assertEqual(user_cart['cart_subtotal'], tp.price*2)
        self.assertEqual(user_cart['cart_subtotal'], user_cart['cart_total'])
        self.assertEqual(user_cart['coupon_applied'], 'no-coupon')
        self.assertEqual(user_cart['chargable_percentage'], 1)
        
    def testCannotAddItemToCartNonExistentProduct(self):
        response = self.client.get('/checkout/cart/add/999/2/')
        self.assertRedirects(
            response,
            '/checkout/cart/',
            status_code=302,
            target_status_code=200
            )    
        session = self.client.session
        self.assertNotIn('user_cart',session)
        
    def testCannotAddItemToCartQuantityTooLarge(self):
        
        response = self.client.get('/checkout/cart/add/1/100000/')
        self.assertRedirects(
            response,
            '/checkout/cart/',
            status_code=302,
            target_status_code=200
            )
        
        session = self.client.session
        self.assertNotIn('user_cart',session)
        
class CheckoutCartEditFunctionTest(TestCase):
    def setUp(self):
        ta = create_test_account()
        ta.set_password('password123')
        ta.save()
        create_test_product(ta.id)
        tp = Product(
            name="Generic Wine 2",
            year=2013,
            description="This is another bottle of Generic Wine",
            price=102,
            quantity_in_stock=100,
            product_picture=DEFAULT_IMAGE_UUID,
            region="FRANCE",
            nodes="Fruits",
            body="Light",
            seller_id=ta.id,
            views=0
            )
        tp.save()
        
    def testCanEditItemInCart(self):
        tp_1 = Product.objects.get(pk=1)
        tp_2 = Product.objects.get(pk=2)
        self.client.get('/checkout/cart/add/1/1/')
        self.client.get('/checkout/cart/add/2/1/')
        
        user_cart = self.client.session['user_cart']
        
        test_form_data = {
            'product-number': ['1', '2'],
            'item-quantity': ['3', '4'],
            'coupon-applied': ['no-coupon'],
            'chargable-percentage': ['1']
        }
        
        response = self.client.post('/checkout/cart/edit/', test_form_data)
        
        self.assertRedirects(
            response,
            '/checkout/cart/',
            status_code=302,
            target_status_code=200
            )    
            
        user_cart = self.client.session['user_cart']
        
        self.assertEqual(user_cart['cart_items'][0]['product_number'], 1)
        self.assertEqual(user_cart['cart_items'][0]['quantity'], 3)
        self.assertEqual(user_cart['cart_items'][1]['product_number'], 2)
        self.assertEqual(user_cart['cart_items'][1]['quantity'], 4)
        self.assertEqual(user_cart['cart_subtotal'], tp_1.price*3+tp_2.price*4)
        self.assertEqual(user_cart['cart_subtotal'], user_cart['cart_total'])
        self.assertEqual(user_cart['coupon_applied'], 'no-coupon')
        self.assertEqual(user_cart['chargable_percentage'], 1)
        
    def testCannotEditItemInCartNonExistentProduct(self):
        tp_1 = Product.objects.get(pk=1)
        tp_2 = Product.objects.get(pk=2)
        self.client.get('/checkout/cart/add/1/1/')
        self.client.get('/checkout/cart/add/2/1/')
        
        user_cart = self.client.session['user_cart']
        
        test_form_data = {
            'product-number': ['1', '3'],
            'item-quantity': ['3', '4'],
            'coupon-applied': ['no-coupon'],
            'chargable-percentage': ['1']
        }
        
        response = self.client.post('/checkout/cart/edit/', test_form_data)
        
        self.assertRedirects(
            response,
            '/checkout/cart/',
            status_code=302,
            target_status_code=200
            )    
            
        user_cart = self.client.session['user_cart']
        
        self.assertEqual(user_cart['cart_items'][0]['product_number'], 1)
        self.assertEqual(user_cart['cart_items'][0]['quantity'], 3)
        self.assertEqual(user_cart['cart_items'][1]['product_number'], 2)
        self.assertEqual(user_cart['cart_items'][1]['quantity'], 1)
        self.assertEqual(user_cart['cart_subtotal'], tp_1.price*3+tp_2.price)
        self.assertEqual(user_cart['cart_subtotal'], user_cart['cart_total'])
        self.assertEqual(user_cart['coupon_applied'], 'no-coupon')
        self.assertEqual(user_cart['chargable_percentage'], 1)
        
    def testCannotEditItemInCartSelectedItemNotInCart(self):
        tp = Product.objects.get(pk=1)
        self.client.get('/checkout/cart/add/1/1/')
        
        user_cart = self.client.session['user_cart']
        
        test_form_data = {
            'product-number': ['2'],
            'item-quantity': ['3'],
            'coupon-applied': ['no-coupon'],
            'chargable-percentage': ['1']
        }
        
        response = self.client.post('/checkout/cart/edit/', test_form_data)
        
        self.assertRedirects(
            response,
            '/checkout/cart/',
            status_code=302,
            target_status_code=200
            )    
            
        user_cart = self.client.session['user_cart']
        
        self.assertEqual(user_cart['cart_items'][0]['product_number'], 1)
        self.assertEqual(user_cart['cart_items'][0]['quantity'], 1)
        self.assertEqual(user_cart['cart_subtotal'], tp.price)
        self.assertEqual(user_cart['cart_subtotal'], user_cart['cart_total'])
        self.assertEqual(user_cart['coupon_applied'], 'no-coupon')
        self.assertEqual(user_cart['chargable_percentage'], 1)
        
    def testCannotEditItemInCartSelectedQuantityTooLarge(self):
        tp = Product.objects.get(pk=1)
        self.client.get('/checkout/cart/add/1/1/')
        
        user_cart = self.client.session['user_cart']
        
        test_form_data = {
            'product-number': ['1'],
            'item-quantity': ['1000000'],
            'coupon-applied': ['no-coupon'],
            'chargable-percentage': ['1']
        }
        
        response = self.client.post('/checkout/cart/edit/', test_form_data)
        
        self.assertRedirects(
            response,
            '/checkout/cart/',
            status_code=302,
            target_status_code=200
            )    
            
        user_cart = self.client.session['user_cart']
        
        self.assertEqual(user_cart['cart_items'][0]['product_number'], 1)
        self.assertEqual(user_cart['cart_items'][0]['quantity'], 1)
        self.assertEqual(user_cart['cart_subtotal'], tp.price)
        self.assertEqual(user_cart['cart_subtotal'], user_cart['cart_total'])
        self.assertEqual(user_cart['coupon_applied'], 'no-coupon')
        self.assertEqual(user_cart['chargable_percentage'], 1)
        
    def testCanApplyValidCouponCode(self):
        create_test_coupon()
        test_form_data = {
            'coupon_code': 'testcoupon'
        }
        
        response = self.client.get('/checkout/coupon/', test_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'discount': 10,
                'status': 'Coupon Applied'
            }
        )
        
    def testCannotApplyInvalidCouponCode(self):
        create_test_coupon()
        test_form_data = {
            'coupon_code': 'testcoupon2'
        }
        
        response = self.client.get('/checkout/coupon/', test_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'discount': None,
                'status': 'Coupon Does Not Exist'
            }
        )
        
class CheckoutCartDeleteFunctionTest(TestCase):
    def setUp(self):
        ta = create_test_account()
        ta.set_password('password123')
        ta.save()
        create_test_product(ta.id)
        tp = Product(
            name="Generic Wine 2",
            year=2013,
            description="This is another bottle of Generic Wine",
            price=102,
            quantity_in_stock=100,
            product_picture=DEFAULT_IMAGE_UUID,
            region="FRANCE",
            nodes="Fruits",
            body="Light",
            seller_id=ta.id,
            views=0
            )
        tp.save()
        
    def testCanDeleteItemFromCart(self):
        tp_1 = Product.objects.get(pk=1)
        self.client.get('/checkout/cart/add/1/1/')
        self.client.get('/checkout/cart/add/2/1/')
        user_cart = self.client.session['user_cart']
        self.assertEqual(len(user_cart['cart_items']), 2)
        
        response = self.client.get('/checkout/cart/delete/2/')
        self.assertRedirects(
            response,
            '/checkout/cart/',
            status_code=302,
            target_status_code=200
            )    
        user_cart = self.client.session['user_cart']
        
        self.assertEqual(len(user_cart['cart_items']), 1)
        self.assertEqual(user_cart['cart_subtotal'], tp_1.price)
        self.assertEqual(user_cart['cart_subtotal'], user_cart['cart_total'])
        
    def testCannotDeleteItemFromCartItemNotInCart(self):
        tp_1 = Product.objects.get(pk=1)
        self.client.get('/checkout/cart/add/1/1/')
        self.client.get('/checkout/cart/delete/2/')
        user_cart = self.client.session['user_cart']
        
        self.assertEqual(len(user_cart['cart_items']), 1)
        self.assertEqual(user_cart['cart_subtotal'], tp_1.price)
        self.assertEqual(user_cart['cart_subtotal'], user_cart['cart_total'])
    
class CheckoutCartClearFunctionTest(TestCase):
    def setUp(self):
        ta = create_test_account()
        ta.set_password('password123')
        ta.save()
        create_test_product(ta.id)
        
    def testCanClearCart(self):
        self.client.get('/checkout/cart/add/1/2/')
        user_cart = self.client.session['user_cart']
        
        self.assertEqual(len(user_cart['cart_items']), 1)
        
        response = self.client.get('/checkout/cart/clear/')
        self.assertRedirects(
            response,
            '/checkout/cart/',
            status_code=302,
            target_status_code=200
            )    
            
        user_cart = self.client.session['user_cart']
        self.assertEqual(user_cart['cart_items'],[])
        self.assertEqual(user_cart['cart_subtotal'], 0)
        self.assertEqual(user_cart['cart_subtotal'], user_cart['cart_total'])
        self.assertEqual(user_cart['coupon_applied'], 'no-coupon')
        self.assertEqual(user_cart['chargable_percentage'], 1)
        
class CustomerDetailCreationTest(TestCase):
    def setUp(self):
        ta = create_test_account()
        ta.set_password('password123')
        ta.save()
        create_test_product(ta.id)
            
    def testValidCustomerDetailCreationSubmission(self):
        test_form_data = {
            'country':'AF',
            'first_name':'John',
            'last_name':'Doe',
            'address_1':"123 Random Road",
            'address_2':"12-34",
            'state_or_country':'Afghanistan',
            'postal_code_or_zip':'123456',
            'email':"johndoe@asd.com",
            'phone':"12345678",
            'account_password':'',
            'alt_country':'',
            'alt_address_1':'', 
            'alt_address_2':'', 
            'alt_state_or_country':'',
            'alt_postal_code_or_zip':'', 
            'order_notes':''
        }

        test_form = CustomerDetailForm(
            data=test_form_data
            )
        
        self.assertTrue(test_form.is_valid())
        self.client.get('/checkout/cart/add/1/1/')
        response = self.client.post('/checkout/checkout/', test_form_data)
        self.assertRedirects(
            response,
            '/checkout/payment/',
            status_code=302,
            target_status_code=200
            ) 
    
    def testInvalidCustomerDetailCreationSubmissionMissingCountry(self):
        test_form_data = {
            'first_name':'John',
            'last_name':'Doe',
            'address_1':"123 Random Road",
            'address_2':"12-34",
            'state_or_country':'Afghanistan',
            'postal_code_or_zip':'123456',
            'email':"johndoe@asd.com",
            'phone':"12345678",
            'account_password':'',
            'alt_country':'',
            'alt_address_1':'', 
            'alt_address_2':'', 
            'alt_state_or_country':'',
            'alt_postal_code_or_zip':'', 
            'order_notes':''
        }

        test_form = CustomerDetailForm(
            data=test_form_data
            )
        self.assertFalse(test_form.is_valid())
        
    def testInvalidCustomerDetailCreationSubmissionMissingFirstName(self):
        test_form_data = {
            'country':'AF',
            'last_name':'Doe',
            'address_1':"123 Random Road",
            'address_2':"12-34",
            'state_or_country':'Afghanistan',
            'postal_code_or_zip':'123456',
            'email':"johndoe@asd.com",
            'phone':"12345678",
            'account_password':'',
            'alt_country':'',
            'alt_address_1':'', 
            'alt_address_2':'', 
            'alt_state_or_country':'',
            'alt_postal_code_or_zip':'', 
            'order_notes':''
        }

        test_form = CustomerDetailForm(
            data=test_form_data
            )
        self.assertFalse(test_form.is_valid())
    
    def testInvalidCustomerDetailCreationSubmissionMissingLastName(self):
        test_form_data = {
            'country':'AF',
            'first_name':'John',
            'address_1':"123 Random Road",
            'address_2':"12-34",
            'state_or_country':'Afghanistan',
            'postal_code_or_zip':'123456',
            'email':"johndoe@asd.com",
            'phone':"12345678",
            'account_password':'',
            'alt_country':'',
            'alt_address_1':'', 
            'alt_address_2':'', 
            'alt_state_or_country':'',
            'alt_postal_code_or_zip':'', 
            'order_notes':''
        }

        test_form = CustomerDetailForm(
            data=test_form_data
            )
        self.assertFalse(test_form.is_valid())
        
    def testInvalidCustomerDetailCreationSubmissionMissingAddress1(self):
        test_form_data = {
            'country':'AF',
            'first_name':'John',
            'last_name':'Doe',
            'address_2':"12-34",
            'state_or_country':'Afghanistan',
            'postal_code_or_zip':'123456',
            'email':"johndoe@asd.com",
            'phone':"12345678",
            'account_password':'',
            'alt_country':'',
            'alt_address_1':'', 
            'alt_address_2':'', 
            'alt_state_or_country':'',
            'alt_postal_code_or_zip':'', 
            'order_notes':''
        }

        test_form = CustomerDetailForm(
            data=test_form_data
            )
        self.assertFalse(test_form.is_valid())
        
    def testInvalidCustomerDetailCreationSubmissionMissingAddress2(self):
        test_form_data = {
            'country':'AF',
            'first_name':'John',
            'last_name':'Doe',
            'address_1':"123 Random Road",
            'state_or_country':'Afghanistan',
            'postal_code_or_zip':'123456',
            'email':"johndoe@asd.com",
            'phone':"12345678",
            'account_password':'',
            'alt_country':'',
            'alt_address_1':'', 
            'alt_address_2':'', 
            'alt_state_or_country':'',
            'alt_postal_code_or_zip':'', 
            'order_notes':''
        }

        test_form = CustomerDetailForm(
            data=test_form_data
            )
        self.assertFalse(test_form.is_valid())
    
    def testInvalidCustomerDetailCreationSubmissionMissingStateOrCountry(self):
        test_form_data = {
            'country':'AF',
            'first_name':'John',
            'last_name':'Doe',
            'address_1':"123 Random Road",
            'address_2':"12-34",
            'postal_code_or_zip':'123456',
            'email':"johndoe@asd.com",
            'phone':"12345678",
            'account_password':'',
            'alt_country':'',
            'alt_address_1':'', 
            'alt_address_2':'', 
            'alt_state_or_country':'',
            'alt_postal_code_or_zip':'', 
            'order_notes':''
        }

        test_form = CustomerDetailForm(
            data=test_form_data
            )
        self.assertFalse(test_form.is_valid())
        
    def testInvalidCustomerDetailCreationSubmissionMissingPostalCodeOrZip(self):
        test_form_data = {
            'country':'AF',
            'first_name':'John',
            'last_name':'Doe',
            'address_1':"123 Random Road",
            'address_2':"12-34",
            'state_or_country':'Afghanistan',
            'email':"johndoe@asd.com",
            'phone':"12345678",
            'account_password':'',
            'alt_country':'',
            'alt_address_1':'', 
            'alt_address_2':'', 
            'alt_state_or_country':'',
            'alt_postal_code_or_zip':'', 
            'order_notes':''
        }

        test_form = CustomerDetailForm(
            data=test_form_data
            )
        self.assertFalse(test_form.is_valid())
        
    def testInvalidCustomerDetailCreationSubmissionMissingEmail(self):
        test_form_data = {
            'country':'AF',
            'first_name':'John',
            'last_name':'Doe',
            'address_1':"123 Random Road",
            'address_2':"12-34",
            'state_or_country':'Afghanistan',
            'postal_code_or_zip':'123456',
            'phone':"12345678",
            'account_password':'',
            'alt_country':'',
            'alt_address_1':'', 
            'alt_address_2':'', 
            'alt_state_or_country':'',
            'alt_postal_code_or_zip':'', 
            'order_notes':''
        }

        test_form = CustomerDetailForm(
            data=test_form_data
            )
        self.assertFalse(test_form.is_valid())
    
    def testInvalidCustomerDetailCreationSubmissionMissingPhone(self):
        test_form_data = {
            'country':'AF',
            'first_name':'John',
            'last_name':'Doe',
            'address_1':"123 Random Road",
            'address_2':"12-34",
            'state_or_country':'Afghanistan',
            'postal_code_or_zip':'123456',
            'email':"johndoe@asd.com",
            'account_password':'',
            'alt_country':'',
            'alt_address_1':'', 
            'alt_address_2':'', 
            'alt_state_or_country':'',
            'alt_postal_code_or_zip':'', 
            'order_notes':''
        }

        test_form = CustomerDetailForm(
            data=test_form_data
            )
        self.assertFalse(test_form.is_valid())
        
    