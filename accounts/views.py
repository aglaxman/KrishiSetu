from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages
# Create your views here.
def register(req):
    if req.method == 'POST':

        form = RegistrationForm(req.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user = Account.objects.create_user(first_name=first_name , last_name = last_name , email=email , username = username,password=password)
            user.phone_number = phone_number
            user.save()
            messages.success(req, 'Registration Successful.')
            return redirect('register')
    else:
        form = RegistrationForm()
    
    context = {
        'form' : form,
    }
    return render(req,'accounts/register.html',context)

def login(req):
    return render(req,'accounts/login.html')

def logout(req):
    return 
# render(req,'accounts/register.html')