from django.shortcuts import render, redirect ,HttpResponse
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required

#verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


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

            #USER ACTIVATION
            current_site = get_current_site(req)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            # messages.success(req, 'Thank you for registration with us. We have sent')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()
    
    context = {
        'form' : form,
    }
    return render(req,'accounts/register.html',context)

def login(req):
    if req.method == 'POST':
        email = req.POST['email']
        password = req.POST['password']
        user = auth.authenticate(email=email,password=password)

        if user is not None:
            auth.login(req,user)
            messages.success(req,'You are now  logged in.')
            return redirect('dashboard')
        else:
            messages.error(req,'Invalid login credentials ')
            return redirect('login')
    return render(req,'accounts/login.html')


@login_required(login_url='login')
def logout(req):
    auth.logout(req)
    messages.success(req,'You are logged out.')
    return redirect('login')



def activate(req, uidb64 , token):
    try: 
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(req,'Congratulations! Your account is activated')
        return redirect('login')
    else:
        messages.error(req,'Invalid activation link')
        return redirect('register')
    



@login_required(login_url='login')
def dashboard(req):
    return render(req,'accounts/dashboard.html')


def forgotPassword(req):
    if req.method == 'POST':
        email = req.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            #reset password email 
            current_site = get_current_site(req)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(req,'Password reset email has been sent to your email address.')
            return redirect('login')

        else:
            messages.error(req,'Account doesnot exist!!')
            return redirect('forgotPassword')
    return render(req,'accounts/forgotpassword.html')



def restpassword_validate(req,uidb64 , token):
    
    try: 
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        req.session['uid'] = uid
        messages.success(req,'Please rest you password')
        return redirect('resetPassword')
    else:
        messages.error(req, 'This link has been expired')
        return redirect('login')
    

def resetPassword(req):
    if req.method == "POST":
        password = req.POST['password']
        confirm_password = req.POST['confirm_password']

        if password == confirm_password:
            uid = req.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(req,'Password reset successful! ')
            return redirect('login')
        else:
            messages.error(req,'Password do not match!')
            return redirect('resetPassword')
            
    return render(req,'accounts/resetpassword.html')