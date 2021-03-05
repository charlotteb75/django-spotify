"""tryDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from pages.views import home_view
from artists.views import artist_list_view, artist_page_view
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    #path('products/<int:my_id>/', dynamic_lookup_view, name='product'),
    #path('create/', product_create_view),
    #path('product_list/', product_list_view),
    #path('products/<int:my_id>/delete/', product_delete_view, name='product-delete'),
    path('search/results/', artist_list_view, name='search-results'),
    path('search/artist/<str:artist_name>', artist_page_view, name='artist-page')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
