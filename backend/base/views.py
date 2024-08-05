from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# Create your views here.

def index(request):
    """home page"""
    return render(request, 'base/index.html')


def loginPage(request):
    """This view handles the login"""
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username/password")

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def registerPage(request):
    """This view handles registration of User"""
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occurred during registration")

    context = {'form': form}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    """log User out"""
    logout(request)
    return redirect('home')