from django.urls import path
from .customer_views import CustomerView
from .organisation_views import OrganisationView
from .transaction_views import TransactionView


urlpatterns = [
    path('organisations/', OrganisationView.as_view()),
    path('organisations/<int:pk>', OrganisationView.as_view()),
    path('customers/', CustomerView.as_view()),
    path('customers/<int:pk>', CustomerView.as_view()),
    path('transactions/', TransactionView.as_view()),
    path('transactions/<int:pk>', TransactionView.as_view()),
]