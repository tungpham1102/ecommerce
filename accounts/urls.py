from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('validate_register/', views.validate_register, name='validate_register'),
    path('user_page/', views.user_page, name='user_page'),
]