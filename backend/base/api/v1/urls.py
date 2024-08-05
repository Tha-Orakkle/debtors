from django.urls import path
from .admin_only_views import TransactionView, UserView
from .customer_views import CustomerView
from .organisation_views import OrganisationView, DebtorsView
from .customer_transaction_views import CustomerTransactionView
from .user_views import UserCreateView, UserLoginView


urlpatterns = [
    # User Creation and Login
    path('create-user/', UserCreateView.as_view()),
    path('login/', UserLoginView.as_view()),

    # For Admins
    path('users/', UserView.as_view()),
    path('transactions/', TransactionView.as_view()),
    path('transactions/<int:pk>', TransactionView.as_view()),

    # For Regular Users
    # CRUD organisation
    path('organisations/', OrganisationView.as_view()),
    path('organisations/<int:pk>', OrganisationView.as_view()),

    # get debtors list
    path('organisation/<int:org_id>/debtors/', DebtorsView.as_view()),

    # CRUD customer
    path('organisation/<int:org_id>/customers/', CustomerView.as_view()),
    path('organisation/<int:org_id>/customers/<int:cus_id>', CustomerView.as_view()),

    # CRUD transactions
    path('organisation/<int:org_id>/customer/<int:cus_id>/transactions', CustomerTransactionView.as_view()),    
    path('organisation/<int:org_id>/customer/<int:cus_id>/transactions/<int:tran_id>', CustomerTransactionView.as_view()),
]