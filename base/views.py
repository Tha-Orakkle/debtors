from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.db.models import Q
from rest_framework.authtoken.models import Token
import requests
import json

from .models import User, Organisation, Customer
from .forms import CreateOrganisationForm, CustomUserCreationForm, UpdateOrganisationForm
from base.backends.decorators import token_required

API_BASE_URL = "http://127.0.0.1:8000/api/v1/"


# Create your views here.
@token_required
def index(request):
    """home page"""
    context = {
        'title': 'Home'
    }
    return render(request, 'base/index.html', context)


def loginPage(request):
    """This view handles the login"""
    page = 'login'
    token = request.COOKIES.get('token')
    
    if token:
        try:
            user_token = Token.objects.get(key=token)
            user = user_token.user
            return redirect('home')
        except:
            pass

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user:
            url = API_BASE_URL + 'token/'
            res = requests.post(url, json={
                'user_id': str(user.id)})
            if res.status_code == 200:
                token = res.json()
                response = redirect('home')
                response.set_cookie('token', token['token'], httponly=True, secure=True, max_age=86400) # live for 1 day
                
                return response
        else:
            messages.error(request, "Invalid username/password")
            return redirect('login')

    context = {'page': page, 'title': 'Login'}
    return render(request, 'base/login_register.html', context)


def registerPage(request):
    """This view handles registration of User"""
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if user.username:
                user.username = user.username.lower()
            user.set_password(request.POST.get('password1'))
            user.save()
            url = API_BASE_URL + 'token/'
            res = requests.post(url, json={'user_id': str(user.id)})
            if res.status_code == 200:
                token = res.json()
                response = redirect('home')
                response.set_cookie('token', token['token'], httponly=True, secure=True, max_age=86400)
                return response
        else:
            for errors in form.errors.values():
                for error in errors:
                    messages.error(request, f"{error}")
            return redirect('register')

    context = {'form': form, 'title': 'Register'}
    return render(request, 'base/login_register.html', context)


@token_required
def logoutUser(request):
    """log User out"""
    token = Token.objects.get(user=request.user)
    token.delete()
    response = redirect('home')
    response.delete_cookie('token')
    return response


@token_required
def create_organisation(request):
    previous_url = request.META.get('HTTP_REFERER')
    form = CreateOrganisationForm()
    if request.method == 'POST':
        token = request.COOKIES.get('token')
        data = {key: value.strip() for key, value in request.POST.items()}
        url = API_BASE_URL + 'organisations/'
        res = requests.post(
            url,
            json=data,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f"Token {token}"
            })
        if res.status_code == 201:
            messages.success(request, "Organisation created successfully!")
            return redirect('home')
        messages.error(request, res.json()['detail'])
        return redirect('create-organisation')
    context = {'form': form, 'title': 'Create New Organisation', 'previous_url': previous_url}
    return render(request, 'base/create-organisation.html', context)


@token_required
def organisation(request, org_id):
    url = API_BASE_URL + f'organisation/{org_id}/debtors/'
    token = request.COOKIES.get('token')
    res = requests.get(url, headers={
        'Authorization': f'Token {token}'})
    if res.status_code != 200:
        messages.error(request, res.json()['detail'])
        return redirect(request.META.get('HTTP_REFERER'))
    data = res.json()
    transactions = data.get('transactions')
    debtors = sorted(transactions, key=lambda x: x['balance'], reverse=True)
    context = {
        'title': data.get('organisation')['name'],
        'organisation': data.get('organisation'),
        'transactions': debtors,
        'customers': data.get('customers')
    }
    return render(request, 'base/organisation.html', context)


@token_required
def update_organisation(request, org_id):
    try:
        organisation = Organisation.objects.get(id=org_id)
    except:
        messages.error(request, "An error occured during the process!")
        return redirect('organisation', org_id)
    form = UpdateOrganisationForm(instance=organisation)
    if request.method == 'POST':
        token = request.COOKIES.get('token')
        data = {key: value.strip() for key, value in request.POST.items()}
        url = API_BASE_URL + f'organisations/{org_id}/'
        res = requests.put(
            url,
            json=data,
            headers={
                'Authorization': f"Token {token}"
            })
        if res.status_code != 200:
            messages.error(request, res.json()['detail'])
            return redirect('update-organisation', org_id)
        messages.success(request, "Organisation successfully updated!")
        return redirect('organisation', org_id)

    context = {
        'title': f'Edit {organisation.name}',
        'organisation': organisation,
        'form': form
    }
    return render(request, 'base/update-organisation.html', context)


@token_required
def create_customer(request, org_id):
    if request.method == 'POST':
        prev_url = request.META['HTTP_REFERER']
        url = API_BASE_URL + f'organisation/{org_id}/customers/'
        token = request.COOKIES.get('token')
        data = {k: v for k, v in request.POST.items()}
        res = requests.post(
            url, json=data,
            headers={
                'Authorization': f'Token {token}'
            }
        )
        if res.status_code != 201:
            messages.error(request, res.json()['detail'])
        else:
            messages.success(request, "New customer created successfully!")
        return redirect(prev_url)
        

@token_required
def customer(request, **kwargs):
    base_url = 'http://127.0.0.1:8000/api/v1/'
    url = base_url + f'organisation/{kwargs['org_id']}/customer/{kwargs['cus_id']}/transactions/'
    token = request.COOKIES.get('token')
    res = requests.get(
        url,
        headers={'Authorization': f'Token {token}'}
    )
    if res.status_code != 200:
        messages.error(request, res.json()['detail'])
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    data = res.json()
    
    customer = data['customer']
    customers = Customer.objects.filter(organisation__id=kwargs['org_id']).order_by('name')
    context = {
        'title': customer['name'],
        'organisation': customer['organisation'],
        'customer': customer,
        'customers': customers,
        'transactions': data['transactions']
    }
    return render(request, 'base/customer.html', context)


@token_required
def create_transaction(request, **kwargs):
    if request.method == 'POST':
        prev_url = request.META['HTTP_REFERER']
        org_id = kwargs.get('org_id')
        
        data = {k: v.strip()  for k, v in request.POST.items()}
        token = request.COOKIES.get('token')
        url = API_BASE_URL + f"organisation/{org_id}/customer/{data['customer_id']}/transactions/"
        res = requests.post(
            url, json=data,
            headers={
                'Authorization': f'Token {token}'
            }
        )
        if res.status_code != 201:
            messages.error(request, res.json()['detail'])
            return redirect(prev_url)
        messages.success(request, "Transaction created successfully!")
        return redirect('customer', org_id=org_id, cus_id=data['customer_id'])
