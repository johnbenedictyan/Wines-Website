from django.test import TestCase
from users.models import UserAccount
from .models import Product
# Product Test Cases
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
    
class ProductTest(TestCase):
    def testCanCreateProduct(self):
        ta = create_account()
        test_product = Product(
            name="Generic Wine",
            year=2013,
            description="This is a bottpe of Generic Wine",
            price=53.99,
            quantity_in_stock=100,
            product_picture=DEFAULT_IMAGE_UUID,
            region="France",
            nodes="Fruits",
            body="Light-Bodied",
            seller_id=ta.id,
            views=0
            )
        test_product.save()
        
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
        ta = create_account()
        test_product = Product(
            name="Generic Wine",
            year=2013,
            description="This is a bottpe of Generic Wine",
            price=53.99,
            quantity_in_stock=100,
            product_picture=DEFAULT_IMAGE_UUID,
            region="France",
            nodes="Fruits",
            body="Light-Bodied",
            seller_id=ta.id,
            views=0
            )
        test_product.save()
        Product.objects.filter(id=test_product.id).delete()
        tp_from_db = list(Product.objects.all().filter(pk=test_product.id))
        self.assertEquals(tp_from_db,[])
    
    def testCanUpdateproductDetails(self):
        ta = create_account()
        test_product = Product(
            name="Generic Wine",
            year=2013,
            description="This is a bottpe of Generic Wine",
            price=53.99,
            quantity_in_stock=100,
            product_picture=DEFAULT_IMAGE_UUID,
            region="France",
            nodes="Fruits",
            body="Light-Bodied",
            seller_id=ta.id,
            views=0
            )
        test_product.save()
        
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
    
class ProductUrlTest(TestCase):
    def setUp(self):
        ta = create_account()
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
    
    def testCanLoadShopPage(self):
        response = self.client.get('/shop/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop.html')
    
    def testCanLoadShopSinglePage(self):
        ta = UserAccount.objects.get(pk=1)
        test_product = Product(
            name="Generic Wine",
            year=2013,
            description="This is a bottpe of Generic Wine",
            price=53.99,
            quantity_in_stock=100,
            product_picture=DEFAULT_IMAGE_UUID,
            region="France",
            nodes="Fruits",
            body="Light-Bodied",
            seller_id=ta.id,
            views=0
            )
        test_product.save()
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
        
class ProductFormTest(TestCase):
    def setUp(self):
        ta = create_account()
        ta.set_password('password123')
        ta.save()
        self.user = ta
        
    def testCan(self):
        pass