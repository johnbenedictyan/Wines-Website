from django.test import TestCase
# Product Test Cases
# Create your tests here.
class ListingTest(TestCase):
    def setUp(self):
        UserAccount.objects.create(
            username="penguinrider",
            password="password123",
            email="asd@asd.com",
            first_name="penguin",
            last_name="rider",
            bio="Hi im a penguinrider",
            profile_picture="default.png"
            )
        ta = UserAccount.objects.get(username="penguinrider")
            
    def testCanCreateListing(self):
        ta = UserAccount(username="penguinrider",password="password123",email="asd@asd.com",first_name="penguin",last_name="rider")
        ta.save()
        test_listing = Listing(name="Bench",description="Rustic Bench, very rustic.",price=53.99,location="Bedok Avenue 1",used=True,seller=ta)
        test_listing.save()
        
        test_lc_1 = ListingCategory(name="furniture",description="""
        Furniture refers to movable objects intended to support various human activities such as seating 
        (e.g., chairs, stools, and sofas), eating (tables), and sleeping (e.g., beds). """)
        
        test_lc_1.save()
        test_listing.categories.add(test_lc_1)
        
        tl_from_db = Listing.objects.all().get(pk=test_listing.id)
        
        self.assertEquals(test_listing.name,tl_from_db.name)
        self.assertEquals(test_listing.description,tl_from_db.description)
        self.assertEquals(test_listing.price,tl_from_db.price)
        self.assertEquals(test_listing.location,tl_from_db.location)
        self.assertEquals(test_listing.used,tl_from_db.used)
        self.assertEquals(tl_from_db.categories.count(),1)
        self.assertEquals(tl_from_db.categories.all()[0].name,"furniture")
        self.assertEquals(tl_from_db.seller.username,ta.username)
        self.assertEquals(tl_from_db.seller.password,ta.password)
        self.assertEquals(tl_from_db.seller.email,ta.email)
        
    def testListingCanHaveManyCategories(self):
        ta = UserAccount(username="penguinrider",password="password123",email="asd@asd.com",first_name="penguin",last_name="rider")
        ta.save()
        test_listing = Listing(name="Bench",description="Rustic Bench, very rustic.",price=53.99,location="Bedok Avenue 1",seller=ta)
        test_listing.save()
        
        test_lc_1 = ListingCategory(name="furniture",description="""
        Furniture refers to movable objects intended to support various human activities such as seating 
        (e.g., chairs, stools, and sofas), eating (tables), and sleeping (e.g., beds). """)
        
        test_lc_1.save()
        
        test_lc_2 = ListingCategory(name="rustic",description="""
        simple and often rough in appearance; typical of the countryside """)
        
        test_lc_2.save()
        
        test_listing.categories.add(test_lc_1,test_lc_2)
        
        tl_from_db = Listing.objects.all().get(pk=test_listing.id)
        
        self.assertEquals(tl_from_db.categories.count(),2)
        self.assertEquals(tl_from_db.categories.all()[0].name,"furniture")
        self.assertEquals(tl_from_db.categories.all()[1].name,"rustic")
        
    def testCanDeleteListing(self):
        ta = UserAccount(username="penguinrider",password="password123",email="asd@asd.com",first_name="penguin",last_name="rider")
        ta.save()
        test_listing = Listing(name="Bench",description="Rustic Bench, very rustic.",price=53.99,location="Bedok Avenue 1",seller=ta)
        test_listing.save()
        
        test_lc_1 = ListingCategory(name="furniture",description="""
        Furniture refers to movable objects intended to support various human activities such as seating 
        (e.g., chairs, stools, and sofas), eating (tables), and sleeping (e.g., beds). """)
        
        test_lc_1.save()
        test_listing.categories.add(test_lc_1)
        
        Listing.objects.filter(id=test_listing.id).delete()
        tl_from_db = list(Listing.objects.all().filter(pk=test_listing.id))
        self.assertEquals(tl_from_db,[])
    
    def testCanUpdateListingDetails(self):
        ta = UserAccount(username="penguinrider",password="password123",email="asd@asd.com",first_name="penguin",last_name="rider")
        ta.save()
        test_listing = Listing(name="Bench",description="Rustic Bench, very rustic.",price=53.99,location="Bedok Avenue 1",seller=ta)
        test_listing.save()
        
        test_listing.name="Stool"
        test_listing.description="Not so rustic stool"
        test_listing.price=14.99
        test_listing.location="Yishun Avenue 2"
        test_listing.save()
        
        tl_from_db = Listing.objects.all().get(pk=test_listing.id)
        self.assertEquals(tl_from_db.name,"Stool")
        self.assertEquals(tl_from_db.description,"Not so rustic stool")
        self.assertEquals(tl_from_db.price,14.99)
        self.assertEquals(tl_from_db.location,"Yishun Avenue 2")
    
    def testCanRemoveCategory(self):
        ta = UserAccount(username="penguinrider",password="password123",email="asd@asd.com",first_name="penguin",last_name="rider")
        ta.save()
        
        test_listing = Listing(name="Bench",description="Rustic Bench, very rustic.",price=53.99,location="Bedok Avenue 1",seller=ta)
        test_listing.save()
        
        test_lc_1 = ListingCategory(name="furniture",description="""
        Furniture refers to movable objects intended to support various human activities such as seating 
        (e.g., chairs, stools, and sofas), eating (tables), and sleeping (e.g., beds). """)
        
        test_lc_1.save()
        
        test_lc_2 = ListingCategory(name="rustic",description="""
        simple and often rough in appearance; typical of the countryside """)
        
        test_lc_2.save()
        
        test_listing.categories.add(test_lc_1,test_lc_2)
        
        tl_from_db = Listing.objects.all().get(pk=test_listing.id)
        
        self.assertEquals(tl_from_db.categories,test_listing.categories)
        
        test_listing.categories.remove(test_lc_1)
        new_tl_from_db = Listing.objects.all().get(pk=test_listing.id)
        
        self.assertEquals(new_tl_from_db.categories.count(),1)
        self.assertEquals(new_tl_from_db.categories.all()[0].name,"rustic")