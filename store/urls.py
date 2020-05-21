from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/', views.cart, name='cart'),

    path('search/', views.search, name='search'),
    path('product_detail/<int:pk>', views.product_detail, name='product_detail'),

    path('update_item/', views.update_item, name='update_item'),
    path('process_order/', views.process_order, name='process_order'),
]