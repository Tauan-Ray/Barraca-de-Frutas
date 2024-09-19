from django.contrib import admin
from django.urls import path
from fruits.views import custom_login, seller_site, list_fruits, search_fruit, logout_user
from salles.views import sale_page, show_order

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', custom_login, name='home'),
    path('seller/', seller_site, name='seller'),
    path('seller/sales/', sale_page, name='sales'),
    path('seller/order/', show_order, name='order'),

    path('list_fruits/', list_fruits, name='list_fruits'),
    path('search_fruit/', search_fruit, name='search_fruit'),
    path('logout/', logout_user, name='logout'),
    
]