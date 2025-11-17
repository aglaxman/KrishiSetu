
# farmers/views.py
from django.shortcuts import render, redirect ,HttpResponse
from .forms import FarmerRegistrationForm
from .models import FarmerAccount
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse

#verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


from carts.views import _cart_id
from carts.models import Cart,CartItem
import requests


def farmer_register(req):

    if req.method == 'POST':
        form = FarmerRegistrationForm(req.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Create farmer user via manager (username auto-generated if manager implementation handles it)
            user = FarmerAccount.objects.create_user(
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                password=password
            )
            # ensure phone saved (manager already sets it, but keep for safety)
            user.phone_number = phone_number
            user.save()

            # USER ACTIVATION EMAIL (same flow as buyer)
            current_site = get_current_site(req)
            mail_subject = 'Please activate your farmer account'
            message = render_to_string('farmers/accounts/account_verification.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            # Redirect to farmer login with message/params (adjust URL as needed)
            return redirect(f"{reverse('farmer_login')}?command=verification&email={email}")
    else:
        form = FarmerRegistrationForm()

    context = {
        'form': form,
        'is_farmer': True,  # optional: let template know this is farmer flow
    }
    return render(req, 'farmers/accounts/register.html', context)
    

def farmer_login(req):
    if req.method == 'POST':
        email = req.POST.get('email')
        password = req.POST.get('password')

        # authenticate using the backends (FarmerBackend should handle FarmerAccount)
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            # Ensure this is a FarmerAccount instance (safety)
            # and that the farmer is verified before allowing login.
            # If you want to allow non-verified farmers to login, remove this check.
            if hasattr(user, 'verified') and not user.verified:
                messages.error(req, 'Your farmer account is not verified yet. Please wait for admin approval.')
                return redirect('/farmers/accounts/login/')

            # Log the user in
            auth.login(req, user)
            messages.success(req, 'You are now logged in.')

            # Preserve the original 'next' redirect if present in referring URL
            url = req.META.get('HTTP_REFERER')
            try:
                if url:
                    query = requests.utils.urlparse(url).query
                    if query:
                        params = dict(x.split('=') for x in query.split('&') if '=' in x)
                        next_page = params.get('next')
                        if next_page:
                            return redirect(next_page)
            except Exception:
                # if anything goes wrong parsing the referrer, fall back to dashboard
                pass

            # Default farmer landing page
            return redirect('farmer_dashboard')
        else:
            messages.error(req, 'Invalid login credentials')
            return redirect('farmers/accounts/login/')  # redirect to farmer login
    # GET request: render shared login template with farmer flag
    return render(req, 'farmers/accounts/login.html', {'is_farmer': True})


@login_required(login_url='farmer_login')
def farmer_logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('farmer_login')



def farmer_activate(req, uidb64 , token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = FarmerAccount._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, FarmerAccount.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True   # allow login after email activation
        user.save()
        messages.success(req, 'Congratulations! Your farmer account is activated.')
        return redirect('farmer_login')
    else:
        messages.error(req, 'Invalid activation link.')
        return redirect('farmer_register')




@login_required(login_url='farmer_login')
def farmer_dashboard(request):
    return render(request, 'farmers/accounts/dashboard.html')


def farmer_forgotPassword(req):
    if req.method == 'POST':
        email = req.POST.get('email')

        if FarmerAccount.objects.filter(email=email).exists():
            user = FarmerAccount.objects.get(email__exact=email)

            # RESET PASSWORD EMAIL
            current_site = get_current_site(req)
            mail_subject = 'Reset Your Farmer Account Password'
            message = render_to_string('farmers/accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            send_email = EmailMessage(mail_subject, message, to=[email])
            send_email.send()

            messages.success(req, 'Password reset email has been sent to your email address.')
            return redirect('farmer_login')

        else:
            messages.error(req, 'Farmer account does not exist!')
            return redirect('farmer_forgotPassword')

    return render(req, 'farmers/accounts/forgotpassword.html', {'is_farmer': True})



def farmer_restpassword_validate(req,uidb64 , token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = FarmerAccount._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, FarmerAccount.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # store uid in session for the reset view to pick up
        req.session['farmer_reset_uid'] = uid
        messages.success(req, 'Please reset your password.')
        return redirect('farmer_resetPassword')
    else:
        messages.error(req, 'This link has expired or is invalid.')
        return redirect('farmer_login')
    

def farmer_resetPassword(req):
            
    if req.method == "POST":
        password = req.POST.get('password')
        confirm_password = req.POST.get('confirm_password')

        if password == confirm_password:
            uid = req.session.get('farmer_reset_uid')   # farmer session key
            if uid is None:
                messages.error(req, "Session expired. Please request a new password reset link.")
                return redirect('farmer_forgotPassword')

            try:
                user = FarmerAccount.objects.get(pk=uid)
            except FarmerAccount.DoesNotExist:
                messages.error(req, "User not found.")
                return redirect('farmer_forgotPassword')

            user.set_password(password)
            user.save()

            # Clear session UID so it cannot be reused
            req.session.pop('farmer_reset_uid', None)

            messages.success(req, 'Password reset successful!')
            return redirect('farmer_login')
        else:
            messages.error(req, 'Passwords do not match!')
            return redirect('farmer_resetPassword')

    return render(req, 'farmers/accounts/resetpassword.html', {'is_farmer': True})
