from django.urls import path
from .customer_views import CustomerView
from .organisation_views import OrganisationView


urlpatterns = [
    path('organisations/', OrganisationView.as_view(), name='organisations'),
    path('organisations/<int:pk>', OrganisationView.as_view(), name='organisations'),
    path('customers/', CustomerView.as_view(), name='customers'),
]