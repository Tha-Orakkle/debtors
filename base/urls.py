from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    
    path('create-organisation/', views.create_organisation, name='create-organisation'),
    path('organisation/<int:org_id>/', views.organisation, name='organisation'),
    path('update-organisation/<int:org_id>/', views.update_organisation, name='update-organisation'),
    
    path('organisation/<int:org_id>/customer/', views.create_customer, name='create-customer'),
    path('organisation/<int:org_id>/customer/<int:cus_id>/', views.customer, name='customer'),
    
    path('organisation/<int:org_id>/customer/transaction/', views.create_transaction, name='create-transaction'),
       
    
]
