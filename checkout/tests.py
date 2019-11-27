from django.test import TestCase
from users.models import UserAccount
from products.models import Product
from .models import Coupon
from datetime import timedelta,datetime
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

class CheckoutCartAddFunctionTest(TestCase):
    def setUp(self):
        ta = create_test_account()
        ta.set_password('password123')
        ta.save()
        create_test_product(ta.id)
        
    def testCanAddItemToCart(self):
        self.client.login(
            username='penguinrider',
            password='password123'
            )
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
        self.client.login(
            username='penguinrider',
            password='password123'
            )
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
        self.client.login(
            username='penguinrider',
            password='password123'
            )
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
        self.client.login(
            username='penguinrider',
            password='password123'
            )
        tp_1 = Product.objects.get(pk=1)
        tp_2 = Product.objects.get(pk=2)
        response = self.client.get('/checkout/cart/add/1/1/')
        response = self.client.get('/checkout/cart/add/2/1/')
        
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
        self.client.login(
            username='penguinrider',
            password='password123'
            )
        
        tp_1 = Product.objects.get(pk=1)
        tp_2 = Product.objects.get(pk=2)
        response = self.client.get('/checkout/cart/add/1/1/')
        response = self.client.get('/checkout/cart/add/2/1/')
        
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
        self.client.login(
            username='penguinrider',
            password='password123'
            )

        tp = Product.objects.get(pk=1)
        response = self.client.get('/checkout/cart/add/1/1/')
        
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
        self.client.login(
            username='penguinrider',
            password='password123'
            )
        
        tp = Product.objects.get(pk=1)
        response = self.client.get('/checkout/cart/add/1/1/')
        
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
        self.client.login(
            username='penguinrider',
            password='password123'
            )
            
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
        self.client.login(
            username='penguinrider',
            password='password123'
            )
            
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
        
class CheckoutCartClearFunctionTest(TestCase):
    def setUp(self):
        ta = create_test_account()
        ta.set_password('password123')
        ta.save()
        create_test_product(ta.id)
        
    def testCanClearCart(self):
        self.client.login(
            username='penguinrider',
            password='password123'
            )
            
        response = self.client.get('/checkout/cart/add/1/2/')
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