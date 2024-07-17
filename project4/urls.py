"""project4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from checkout.urls import urlpatterns as checkout_urls
from products.urls import urlpatterns as products_urls
from users.urls import urlpatterns as users_urls
from website.urls import urlpatterns as website_urls
from website.views import handler404 as handler404_view_function

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^checkout/', include(checkout_urls)),
    re_path(r'^shop/', include(products_urls)),
    re_path(r'^users/', include(users_urls)),
    re_path(r'^', include(website_urls)),
]

if settings.DEBUG:  # new
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

handler404 = handler404_view_function
