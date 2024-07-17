from django.conf.urls import url
from django.urls import path
from .views import main_page, about_us, contact_us, blog_creator, bloghub, single_blog

urlpatterns = [
    path('', main_page, name="main_page"),
    path('about-us/', about_us, name="about_us"),
    path('contact-us/', contact_us, name="contact_us"),
    path('blog/<int:blog_number>/', single_blog, name="single_blog"),
    path('blog/create/', blog_creator, name="blog_creator"),
    path('blog/', bloghub, name="bloghub"),
]
