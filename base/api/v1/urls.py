from django.urls import path
from .customer_views import CustomerView
from .organisation_views import OrganisationView
from .transaction_views import TransactionView, DebtorsView
from .customer_transaction_views import CustomerTransactionView
from .user_views import UserCreateView, UserLoginView, UserView


urlpatterns = [
    path('create-user/', UserCreateView.as_view()),
    path('login/', UserLoginView.as_view()),
    
    path('debtors/', DebtorsView.as_view()),

    path('users/', UserView.as_view()),

    path('organisations/', OrganisationView.as_view()),
    path('organisations/<int:pk>', OrganisationView.as_view()),

    path('customers/', CustomerView.as_view()),
    path('customers/<int:pk>', CustomerView.as_view()),

    path('transactions/', TransactionView.as_view()),
    path('transactions/<int:pk>', TransactionView.as_view()),

    path('customer/<int:pk>/transactions', CustomerTransactionView.as_view()),    
    path('customer/<int:pk>/transactions/<int:tran_id>', CustomerTransactionView.as_view()),
    

]