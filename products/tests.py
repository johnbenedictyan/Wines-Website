from django.test import TestCase
from django.contrib import auth
from users.models import UserAccount
from .models import Product
from .forms import ProductForm
# Product Test Cases
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
    
class ProductTest(TestCase):
    def testCanCreateProduct(self):
        ta = create_test_account()
        test_product = create_test_product(ta.id)
        
        tp_from_db = Product.objects.all().get(pk=test_product.id)
        
        self.assertEquals(
            test_product.name,
            tp_from_db.name
            )
        self.assertEquals(
            test_product.year,
            tp_from_db.year
            )
        self.assertEquals(
            test_product.description,
            tp_from_db.description
            )
        self.assertEquals(
            test_product.price,
            tp_from_db.price
            )
        self.assertEquals(
            test_product.quantity_in_stock,
            tp_from_db.quantity_in_stock
            )
        self.assertEquals(
            test_product.region,
            tp_from_db.region
            )
        self.assertEquals(
            test_product.nodes,
            tp_from_db.nodes
            )
        self.assertEquals(
            test_product.body,
            tp_from_db.body
            )
        self.assertEquals(
            test_product.views,
            tp_from_db.views
            )
        self.assertEquals(
            tp_from_db.seller_id,
            ta.id
            )
        
    def testCanDeleteproduct(self):
        ta = create_test_account()
        test_product = create_test_product(ta.id)
        Product.objects.filter(id=test_product.id).delete()
        tp_from_db = list(Product.objects.all().filter(pk=test_product.id))
        self.assertEquals(tp_from_db,[])
    
    def testCanUpdateproductDetails(self):
        ta = create_test_account()
        test_product = create_test_product(ta.id)
        
        test_product.name="Generic Wine 2"
        test_product.description="A different kind of generic"
        test_product.price=14.99
        test_product.save()
        
        tp_from_db = Product.objects.all().get(pk=test_product.id)
        self.assertEquals(
            tp_from_db.name,
            "Generic Wine 2"
            )
        self.assertEquals(
            tp_from_db.description,
            "A different kind of generic"
            )
        self.assertEquals(
            tp_from_db.price,
            14.99
            )
    
class ProductUrlGeneralTest(TestCase):
    def setUp(self):
        ta = create_test_account()
        ta.set_password('password123')
        ta.save()
        
    def testCanLoadInventoryPageWithLogin(self):
        self.client.login(
            username='penguinrider',
            password='password123'
            )
        response = self.client.get('/shop/products/inventory/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory.html')
            
    def testCannotLoadInventoryPageWithoutLogin(self):
        response = self.client.get('/shop/products/inventory/')
        self.assertRedirects(
            response,
            '/users/log-in/?next=/shop/products/inventory/',
            status_code=302,
            target_status_code=200
            )
    
    def testCanLoadShopPage(self):
        response = self.client.get('/shop/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop.html')
    
    def testCanLoadShopSinglePage(self):
        ta = UserAccount.objects.get(pk=1)
        create_test_product(ta.id)
        response = self.client.get('/shop/products/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop-single.html')
        
    def testCannotLoadNonExistentShopSinglePage(self):
        response = self.client.get('/shop/products/1/')
        self.assertRedirects(
            response,
            '/shop/',
            status_code=302,
            target_status_code=200
            )
    
    def testCanLoadBestSellersPage(self):
        response = self.client.get('/shop/collection/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wine-collection.html')
        
class ProductUrlCreationTest(TestCase):
    def setUp(self):
        ta = create_test_account()
        ta.set_password('password123')
        ta.save()
        
    def testCanLoadProductCreationPage(self):
        self.client.login(
            username='penguinrider',
            password='password123'
            )
        response = self.client.get('/shop/products/create/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product-form.html')
        
    def testCannotLoadProductCreationPageWithoutLogin(self):
        response = self.client.get('/shop/products/create/')
        self.assertRedirects(
            response,
            '/users/log-in/?next=/shop/products/create/',
            status_code=302,
            target_status_code=200
            )
            
class ProductUrlUpdateTest(TestCase):
    def setUp(self):
        ta = create_test_account()
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
        
    def testCannotLoadProductUpdatePageWithoutLogin(self):
        response = self.client.get('/shop/products/update/1/')
        self.assertRedirects(
            response,
            '/users/log-in/?next=/shop/products/update/1/',
            status_code=302,
            target_status_code=200
            )
            
    def testCannotLoadProductUpdatePageForNonExistentProduct(self):
        self.client.login(
            username='penguinrider',
            password='password123'
            )
        response = self.client.get('/shop/products/update/999/')
        self.assertRedirects(
            response,
            '/shop/products/inventory/',
            status_code=302,
            target_status_code=200
            )
    
    def testCannotLoadProductUpdatePageUnauthorisedUser(self):
        self.client.login(
            username='penguinrider2',
            password='password123'
            )
        response = self.client.get('/shop/products/update/1/')
        self.assertRedirects(
            response,
            '/shop/products/inventory/',
            status_code=302,
            target_status_code=200
            )
            
class ProductUrlDeleteTest(TestCase):
    def setUp(self):
        ta = create_test_account()
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
        
    def testCannotLoadProductDeletePageWithoutLogin(self):
        response = self.client.get('/shop/products/delete/1/')
        self.assertRedirects(
            response,
            '/users/log-in/?next=/shop/products/delete/1/',
            status_code=302,
            target_status_code=200
            )
            
    def testCannotLoadProductDeletePageForNonExistentProduct(self):
        self.client.login(
            username='penguinrider',
            password='password123'
            )
        response = self.client.get('/shop/products/delete/1/')
        self.assertRedirects(
            response,
            '/shop/products/inventory/',
            status_code=302,
            target_status_code=200
            )
    
    def testCannotLoadProductDeletePageUnauthorisedUser(self):
        self.client.login(
            username='penguinrider2',
            password='password123'
            )
        response = self.client.get('/shop/products/delete/1/')
        self.assertRedirects(
            response,
            '/shop/products/inventory/',
            status_code=302,
            target_status_code=200
            )
        self.assertEqual(Product.objects.filter(pk=1).count(), 1)
    
    def testCanLoadProductDeletePageAndDelete(self):
        self.client.login(
            username='penguinrider',
            password='password123'
            )
        response = self.client.get('/shop/products/delete/1/')
        self.assertRedirects(
            response,
            '/shop/products/inventory/',
            status_code=302,
            target_status_code=200
            )
        self.assertEqual(Product.objects.filter(pk=1).count(), 0)
    
class ProductFormCreationTest(TestCase):
    def setUp(self):
        ta = create_test_account()
        ta.set_password('password123')
        ta.save()
        self.client.login(
            username='penguinrider',
            password='password123'
            )
        
    def testValidProductFormCreationSubmission(self):
        user = auth.get_user(self.client)
        test_form_data = {
            'name':"Generic Wine",
            'year':2013,
            'description':"This is a bottle of Generic Wine",
            'price':53.99,
            'quantity_in_stock':100,
            'product_picture':DEFAULT_IMAGE_UUID,
            'region':"FRANCE",
            'nodes':"Fruits",
            'body':"Light",
            'seller_id':user.id,
            'views':0
        }
        test_form = ProductForm(
            data=test_form_data
            )
        
        self.assertTrue(test_form.is_valid())
        
    def testMissingNameErrorMessage(self):
        user = auth.get_user(self.client)
        test_form_data = {
            'year':2013,
            'description':"This is a bottle of Generic Wine",
            'price':53.99,
            'quantity_in_stock':100,
            'product_picture':DEFAULT_IMAGE_UUID,
            'region':"FRANCE",
            'nodes':"Fruits",
            'body':"Light",
            'seller_id':user.id,
            'views':0
        }
        test_form = ProductForm(
            data=test_form_data
            )
        self.assertFalse(test_form.is_valid())
        response = self.client.post('/shop/products/create/', test_form_data)
        self.assertFormError(
            response,
            'product_form',
            'name',
            'This field is required.'
            )
        
    def testMissingYearErrorMessage(self):
        user = auth.get_user(self.client)
        test_form_data = {
            'name':"Generic Wine",
            'description':"This is a bottle of Generic Wine",
            'price':53.99,
            'quantity_in_stock':100,
            'product_picture':DEFAULT_IMAGE_UUID,
            'region':"FRANCE",
            'nodes':"Fruits",
            'body':"Light",
            'seller_id':user.id,
            'views':0
        }
        test_form = ProductForm(
            data=test_form_data
            )
        self.assertFalse(test_form.is_valid())
        response = self.client.post('/shop/products/create/', test_form_data)
        self.assertFormError(
            response,
            'product_form',
            'year',
            'This field is required.'
            )
    
    def testMissingDescriptionErrorMessage(self):
        user = auth.get_user(self.client)
        test_form_data = {
            'name':"Generic Wine",
            'year':2013,
            'price':53.99,
            'quantity_in_stock':100,
            'product_picture':DEFAULT_IMAGE_UUID,
            'region':"FRANCE",
            'nodes':"Fruits",
            'body':"Light",
            'seller_id':user.id,
            'views':0
        }
        test_form = ProductForm(
            data=test_form_data
            )
        self.assertFalse(test_form.is_valid())
        response = self.client.post('/shop/products/create/', test_form_data)
        self.assertFormError(
            response,
            'product_form',
            'description',
            'This field is required.'
            )
    
    def testMissingPriceErrorMessage(self):
        user = auth.get_user(self.client)
        test_form_data = {
            'name':"Generic Wine",
            'year':2013,
            'description':"This is a bottle of Generic Wine",
            'quantity_in_stock':100,
            'product_picture':DEFAULT_IMAGE_UUID,
            'region':"FRANCE",
            'nodes':"Fruits",
            'body':"Light",
            'seller_id':user.id,
            'views':0
        }
        test_form = ProductForm(
            data=test_form_data
            )
        self.assertFalse(test_form.is_valid())
        response = self.client.post('/shop/products/create/', test_form_data)
        self.assertFormError(
            response,
            'product_form',
            'price',
            'This field is required.'
            )
    
    def testMissingQuantityInStockErrorMessage(self):
        user = auth.get_user(self.client)
        test_form_data = {
            'name':"Generic Wine",
            'year':2013,
            'description':"This is a bottle of Generic Wine",
            'price':53.99,
            'product_picture':DEFAULT_IMAGE_UUID,
            'region':"FRANCE",
            'nodes':"Fruits",
            'body':"Light",
            'seller_id':user.id,
            'views':0
        }
        test_form = ProductForm(
            data=test_form_data
            )
        self.assertFalse(test_form.is_valid())
        response = self.client.post('/shop/products/create/', test_form_data)
        self.assertFormError(
            response,
            'product_form',
            'quantity_in_stock',
            'This field is required.'
            )
            
    def testMissingProductPictureErrorMessage(self):
        user = auth.get_user(self.client)
        test_form_data = {
            'name':"Generic Wine",
            'year':2013,
            'description':"This is a bottle of Generic Wine",
            'price':53.99,
            'quantity_in_stock':100,
            'region':"FRANCE",
            'nodes':"Fruits",
            'body':"Light",
            'seller_id':user.id,
            'views':0
        }
        test_form = ProductForm(
            data=test_form_data
            )
        self.assertFalse(test_form.is_valid())
        response = self.client.post('/shop/products/create/', test_form_data)
        self.assertFormError(
            response,
            'product_form',
            'product_picture',
            'This field is required.'
            )
    
    def testMissingRegionErrorMessage(self):
        user = auth.get_user(self.client)
        test_form_data = {
            'name':"Generic Wine",
            'year':2013,
            'description':"This is a bottle of Generic Wine",
            'price':53.99,
            'quantity_in_stock':100,
            'product_picture':DEFAULT_IMAGE_UUID,
            'nodes':"Fruits",
            'body':"Light",
            'seller_id':user.id,
            'views':0
        }
        test_form = ProductForm(
            data=test_form_data
            )
        self.assertFalse(test_form.is_valid())
        response = self.client.post('/shop/products/create/', test_form_data)
        self.assertFormError(
            response,
            'product_form',
            'region',
            'This field is required.'
            ) 
    
    def testMissingNodeErrorMessage(self):
        user = auth.get_user(self.client)
        test_form_data = {
            'name':"Generic Wine",
            'year':2013,
            'description':"This is a bottle of Generic Wine",
            'price':53.99,
            'quantity_in_stock':100,
            'product_picture':DEFAULT_IMAGE_UUID,
            'region':"FRANCE",
            'body':"Light",
            'seller_id':user.id,
            'views':0
        }
        test_form = ProductForm(
            data=test_form_data
            )
        self.assertFalse(test_form.is_valid())
        response = self.client.post('/shop/products/create/', test_form_data)
        self.assertFormError(
            response,
            'product_form',
            'nodes',
            'This field is required.'
            ) 
            
    def testMissingBodyErrorMessage(self):
        user = auth.get_user(self.client)
        test_form_data = {
            'name':"Generic Wine",
            'year':2013,
            'description':"This is a bottle of Generic Wine",
            'price':53.99,
            'quantity_in_stock':100,
            'product_picture':DEFAULT_IMAGE_UUID,
            'region':"FRANCE",
            'nodes':"Fruits",
            'seller_id':user.id,
            'views':0
        }
        test_form = ProductForm(
            data=test_form_data
            )
        self.assertFalse(test_form.is_valid())
        response = self.client.post('/shop/products/create/', test_form_data)
        self.assertFormError(
            response,
            'product_form',
            'body',
            'This field is required.'
            ) 
            
    def testMissingSellerIDErrorMessage(self):
        test_form_data = {
            'name':"Generic Wine",
            'year':2013,
            'description':"This is a bottle of Generic Wine",
            'price':53.99,
            'quantity_in_stock':100,
            'product_picture':DEFAULT_IMAGE_UUID,
            'region':"FRANCE",
            'nodes':"Fruits",
            'body':"Light",
            'views':0
        }
        test_form = ProductForm(
            data=test_form_data
            )
        self.assertFalse(test_form.is_valid())
        response = self.client.post('/shop/products/create/', test_form_data)
        self.assertFormError(
            response,
            'product_form',
            'seller_id',
            'This field is required.'
            ) 
            
    def testInvalidQuantityInStockErrorMessage(self):
        user = auth.get_user(self.client)
        test_form_data = {
            'name':"Generic Wine",
            'year':2013,
            'description':"This is a bottle of Generic Wine",
            'price':53.99,
            'quantity_in_stock':'This is not a number',
            'product_picture':DEFAULT_IMAGE_UUID,
            'region':"FRANCE",
            'nodes':"Fruits",
            'body':"Light",
            'seller_id':user.id,
            'views':0
        }
        test_form = ProductForm(
            data=test_form_data
            )
        
        self.assertFalse(test_form.is_valid())
        response = self.client.post('/shop/products/create/', test_form_data)
        self.assertFormError(
            response,
            'product_form',
            'quantity_in_stock',
            'Enter a whole number.'
            ) 
            
class ProductFormUpdateTest(TestCase):
    def setUp(self):
        ta = create_test_account()
        ta.set_password('password123')
        ta.save()
        create_test_product(ta.id)
        
        self.client.login(
            username='penguinrider',
            password='password123'
            )
        
    def ValidProductFormUpdateSubmission(self):
        test_form_data = {
            'name':"Generic Wine 2",
            'year':2015,
            'description':"This is a bottle of Generic Wine",
            'price':192.62,
            'quantity_in_stock':150,
            'product_picture':DEFAULT_IMAGE_UUID,
            'region':"FRANCE",
            'nodes':"Fruits",
            'body':"Medium"
        }
        
        response = self.client.post(
            '/shop/products/update/1/',
            test_form_data
            )
        self.assertRedirects(
            response,
            '/shop/products/inventory/',
            status_code=302,
            target_status_code=200
            )
        test_product = Product.objects.get(pk=1)
        test_product.refresh_from_db()
        self.assertEquals(
            test_product.name,
            test_form_data['name']
            )
        self.assertEquals(
            test_product.year,
            test_form_data['year']
            )
        self.assertEquals(
            test_product.price,
            test_form_data['price']
            )
        self.assertEquals(
            test_product.body,
            test_form_data['body']
            )