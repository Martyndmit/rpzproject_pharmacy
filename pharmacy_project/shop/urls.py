from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('medicine/<slug:slug>/', views.medicine_detail, name='medicine_detail'),
    path('symptoms/', views.symptom_search, name='symptom_search'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:medicine_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:medicine_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.order_create, name='order_create'),
]
