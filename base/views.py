from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.shortcuts import render, redirect
import requests

from .models import User
from .forms import CustomUserCreationForm
from base.backends.decorators import token_required


# Create your views here.
@token_required
def index(request):
    """home page"""
    return render(request, 'base/index.html')


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
            res = requests.post('http://127.0.0.1:8000/api/v1/token/', data={
                'user_id': user.id})
            if res.status_code == 200:
                token = res.json()
                response = redirect('home')
                response.set_cookie('token', token['token'], httponly=True, secure=True, max_age=86400) # live for 1 day
                
                return response
        else:
            messages.error(request, "Invalid username/password")
            return redirect('login')

    context = {'page': page}
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
            res = requests.post('http://127.0.0.1:8000/api/v1/token/', data={
                'user_id': user.id})
            if res.status_code == 200:
                token = res.json()
                response = redirect('home')
                response.set_cookie('token', token['token'], httponly=True, secure=True, max_age=86400)
                return response
        else:
            messages.error(request, "An error occurred during registration")
            return redirect('register')

    context = {'form': form}
    return render(request, 'base/login_register.html', context)


@token_required
def logoutUser(request):
    """log User out"""
    token = Token.objects.get(user=request.user)
    token.delete()
    response = redirect('home')
    response.delete_cookie('token')
    return response