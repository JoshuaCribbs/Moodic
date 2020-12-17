from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from .forms import CreateAccountForm

def loginPage(request):
    # Defines login endpoint using django's built in authentication
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'account/LoginPage.html')
    #When index is activated home.html is rendered.

def createAccount(request):
    # Defines account creation endpoint using Django's built in form
    form = CreateAccountForm()

    if request.method =='POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'account/CreateAccount.html', context)

def forgotPassword(request):
    # Used to render the forgot password page
    return render(request, 'account/ForgotPassword.html')

def logoutUser(request):
    # Used to handle logout requests and redirect to login page
    logout(request)
    return redirect('loginPage')