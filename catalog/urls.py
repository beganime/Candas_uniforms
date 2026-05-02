from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),
    path('o-kompanii/', views.about, name='about'),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<slug:slug>/', views.product_detail, name='product_detail'),
    path('zayavka/', views.create_request, name='create_request'),
    path('zayavka/uspeshno/', views.contact_success, name='contact_success'),
]
