# Wines
As the saying goes, "Beer is made by men, wine by God", discover the best wines at wines.
## UX
List of User Stories
- As a wine seller, I want to publish a listing, so that I can sell wine.
- As someone who wants to buy wine, I want to search for wine, so that I can find the one that appeals to me.

## Features
### Existing Features
- Listing Creation - Allows users to create their own listings, by having them fill up a listing creation form.
- Listing Updating - Allows users to update their own listings, by having them fill up a listing update form.
- Listing Deletion - Allows users to delete their own listings, with checks in place if they try to delete a listing they did not create.
- Searching for listings - Allows users to search for listings, by having them type in a search bar.
- User Creation - Allows users to create user accounts, by having them fill up a user creation form.
- User Account Details Updating - Allows users to update their user details, by having them fill up a user details updating form.
- User Deletion - Allows users to create their own listings, by having them fill up a listing creation form.
- User & Listing Photo Upload - Allows the user to upload photos for their listings as well as their profiles, by storing the photos on uploadcare.

### Features Left to Implement
- Blog Section: A fully functioning blog section with comments
- Admin Console: A functional admin console on a webpage

## Technologies Used
- [Boostrap](https://getbootstrap.com/)
    - The project uses **Boostrap** to create a mobile responsive and stylish webpage.
- [JQuery](https://jquery.com)
    - The project uses **JQuery** to simplify DOM manipulation.
- [Django](https://www.djangoproject.com/)
    - The project uses **Django** as it's main framework.
- [Pillow](https://pypi.org/project/Pillow/)
    - The project uses **Pillow** to allow for the uploading of photos to AWS S3.
- [coverage](https://coverage.readthedocs.io/en/v4.5.x/)
    - The project uses **coverage** to allow for test coverages to be generated.
- [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
    - The project uses **boto3** to allow for the uploading of photos to AWS S3.
- [botocore](https://pypi.org/project/botocore/)
    - The project uses **botocore** to allow for the uploading of photos to AWS S3.
- [dj-database-url](https://pypi.org/project/dj-database-url/)
    - The project uses **dj-database-url** to allow django to communicate with Heroku's Postgresql.
- [django-crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/)
    - The project uses **django-crispy-forms** to allow for forms to be render in a bootstrap template.
- [gunicorn](https://gunicorn.org/)
    - The project uses **gunicorn** as a python WSGI HTTP server to deploy the app on Heroku.
- [django-storages](https://django-storages.readthedocs.io/en/latest/)
    - The project uses **django-storages** to allow for the uploading of photos to AWS S3.
- [docutils](https://pypi.org/project/docutils/)
    - The project uses **docutils** to process documentation into useful formats, such as HTML, XML, and LaTeX. 
- [python-dateutil](https://pypi.org/project/python-dateutil/)
    - The project uses **python-dateutil** to allow python to get the current date.
- [urllib3](https://urllib3.readthedocs.io/en/latest/)
    - The project uses **urllib3** as a HTTP client.
- [jmespath](http://jmespath.org/)
    - The project uses **jmespath** as a query language for JSON.
- [psycopg2](https://pypi.org/project/psycopg2/)
    - The project uses **psycopg2** to allow django to communicate with Heroku's Postgresql.
- [pytz](https://pypi.org/project/pytz/)
    - The project uses **pytz** to allow for more accurate and cross platform timezone calculations.
- [whitenoise](http://whitenoise.evans.io/en/stable/)
    - The project uses **whitenoise** to allow static files to be served from AWS s3.
- [Stripe](https://stripe.com/)
    - The project uses **Stripe** to process credit card payment.
- [Axios](https://github.com/axios/axios/)
    - The project uses **Stripe** to simplify AJAX calls.
- [pyuploadcare](https://github.com/uploadcare/pyuploadcare/)
    - The project uses **pyuploadcare** to integrate django and UploadCare to upload photos.
- [uploadcare](https://uploadcare.com/)
    - The project uses **uploadcare** to upload and serve images.

## Testing
### Manual Testing:

### Automated Testings:

#### Checkout
- All of the **urls** for this app was tested to be working.
- **Cart**  
    - Creation of the Cart was tested.
    - Reading the data from the Cart was tested.
    - Updating the Cart was tested. 
    - Deleting the entire Cart and specific items was tested. 
- **Order**
    - Creation of an Order was tested.
    - Reading the data from an Order was tested. 

- **Quantity Reducer Function**
    - Able to reduce quantity of stock was tested.
- **Customer Detail Form**
    - The form was tested for both Valid and Missing Fields state.
- **Payment Form** 
    - The form was tested for both Valid and Missing Fields state.
    - Custom Errors generated by Stripe

#### Products
- All of the **urls** for this app was tested to be working.
- All of the **webpages** for this app was tested to be working.
- Creation of Products was tested.
- Reading the data of each individual Product was tested.
- Updating Product details was tested.
- Deletion of Products was tested.

- **Product Form** 
    - The form was tested for both Valid and Missing Fields state.

#### Users
- All of the **urls** for this app was tested to be working.
- All of the **webpages** for this app was tested to be working.
- Creation of Users was tested.
- Reading the data of each individual User was tested.
- Updating User details was tested.
- Deletion of Users was tested.

- **RegisterForm** 
    - The form was tested for both Valid and Missing Fields state.
- Login and Logout was tested.

#### Website
- All of the **urls** for this app was tested to be working.
- All of the **webpages** for this app was tested to be working.
- **Contact Form** 
    - The form was tested for both Valid and Missing Fields state.
- **Blogs**
    - Creation of UseBlogsrs was tested.
    - Reading the data of each individual Blog was tested.
    - Updating Blog details was tested.
    
- **Blog Form**
    - The form was tested for both Valid and Missing Fields state.

### Interesting Bugs/Problems:

## Deployment
On the development version, sensitive information is stored in an env.py that is not pushed to github.
Where as on the deployed version, these sensitive information are stored in the Heroku Config Vars

To run the app locally:
1. Open the terminal.
2. Run this command.
```sh
$ python manage.py runserver <INSERT_YOUR_OWN_SERVER_IP>:<INSERT_YOUR_OWN_SERVER_PORT>
```
3. Click on the local host link address to open the app the web browser.

You can view the deployed version on [Heroku](https://jby-tgc-project-4.herokuapp.com/)
## Credits

### Content

### Media
- The photos used in this site were obtained from [Stock Snap](https://stocksnap.io/),[Pexels](https://www.pexels.com/),[Unsplash](https://unsplash.com/),[Pixabay](https://pixabay.com/)

### Acknowledgements

- The Boostrap Template was taken from [ColorLib](https://colorlib.com/wp/templates/)

