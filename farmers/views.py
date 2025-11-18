
# farmers/views.py
from django.shortcuts import render, redirect ,HttpResponse
from .forms import FarmerRegistrationForm
from .models import FarmerAccount
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.utils.http import url_has_allowed_host_and_scheme
from urllib.parse import urlparse, parse_qs
from django.utils.text import slugify
from store.models import Product
from category.models import Category

#verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from .forms import FarmerProductForm
from .models import FarmerProduct, FarmerAccount

from carts.views import _cart_id
from carts.models import Cart,CartItem
import requests



from .forms import FarmerProductForm
from .models import FarmerProduct


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
        email = req.POST.get('email', '').strip().lower()
        password = req.POST.get('password', '')

        # Basic required-field validation
        if not email or not password:
            messages.error(req, 'Please provide both email and password.')
            return render(req, 'farmers/accounts/login.html', {'is_farmer': True})

        # Authenticate using both possible login parameters
        user = auth.authenticate(req, email=email, password=password) \
               or auth.authenticate(req, username=email, password=password)

        if user is not None:

            # Check active status
            if not getattr(user, 'is_active', False):
                messages.error(req, 'Your account is not active. Please verify your email or contact admin.')
                return render(req, 'farmers/accounts/login.html', {'is_farmer': True})

            # Check farmer "verified" status
            verified_flag = getattr(user, 'verified', None)
            if verified_flag is not None and not verified_flag:
                messages.error(req, 'Your farmer account is not verified yet. Please wait for admin approval.')
                return render(req, 'farmers/accounts/login.html', {'is_farmer': True})

            # Successful login
            auth.login(req, user)
            messages.success(req, 'You are now logged in.')

            # Handle "next" redirects
            next_page = req.POST.get('next') or req.GET.get('next')
            if not next_page:
                ref = req.META.get('HTTP_REFERER')
                if ref:
                    try:
                        parsed = urlparse(ref)
                        qs = parse_qs(parsed.query)
                        next_vals = qs.get('next')
                        if next_vals:
                            next_page = next_vals[0]
                    except Exception:
                        next_page = None

            if next_page and url_has_allowed_host_and_scheme(next_page, allowed_hosts={req.get_host()}):
                return redirect(next_page)

            return redirect('farmer_dashboard')

        else:
            # Wrong credentials
            messages.error(req, 'Invalid login credentials')
            return render(req, 'farmers/accounts/login.html', {'is_farmer': True})

    # GET request
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




@login_required(login_url='farmer_login')
def farmer_dashboard(request):
    # Empty form for the Add Product modal
    form = FarmerProductForm()

    # Optional: fetch farmer’s existing listings (you may use later)
    farmer = request.user
    farmer_products = FarmerProduct.objects.filter(farmer=farmer)

    context = {
        'form': form,                  # required so modal works
        'farmer_products': farmer_products,  # optional for dashboard listing
    }
    return render(request, 'farmers/accounts/dashboard.html', context)


@login_required(login_url='farmer_login')
def farmer_add_product(request):
    """
    Accept two kinds of submission:
    1) FarmerProductForm (select an existing Product and add price/stock)
    2) Plain form fields to create a new Product (name, category, price, quantity, description, image)
       -> creates a new store.Product and then creates a FarmerProduct linking it to the farmer.
    """
    # Resolve farmer instance defensively: request.user may be accounts.Account or FarmerAccount
    user = request.user
    if not hasattr(user, 'verified') and hasattr(user, 'email'):
        try:
            user = FarmerAccount.objects.get(email__iexact=user.email)
        except FarmerAccount.DoesNotExist:
            user = None

    # Provide categories to the template (for plain-create flow)
    categories = Category.objects.all().order_by('category_name') if hasattr(Category, 'objects') else Category.objects.all()

    if request.method == 'POST':
        # CASE A: FarmerProductForm-style submission (select existing product)
        # We detect it by presence of 'product' field in POST (product = Product.pk)
        if 'product' in request.POST and request.POST.get('product'):
            form = FarmerProductForm(request.POST, request.FILES)
            if form.is_valid():
                product = form.cleaned_data['product']
                price = form.cleaned_data['price']
                stock = form.cleaned_data['stock']
                image = form.cleaned_data.get('image')
                is_active = form.cleaned_data.get('is_active', True)

                if user is None:
                    messages.error(request, 'Could not resolve farmer account. Please contact admin.')
                    return redirect('farmer_dashboard')

                obj, created = FarmerProduct.objects.get_or_create(
                    farmer=user,
                    product=product,
                    defaults={'price': price, 'stock': stock, 'image': image, 'is_active': is_active}
                )
                if not created:
                    obj.price = price
                    obj.stock = stock
                    if image:
                        obj.image = image
                    obj.is_active = is_active
                    obj.save()
                    messages.success(request, 'Your listing was updated.')
                else:
                    messages.success(request, 'Product added to your offerings.')

                return redirect('farmer_dashboard')
            else:
                # form errors -> re-render dashboard with form to show errors
                messages.error(request, 'Please correct the errors in the form.')
                context = {'form': form, 'categories': categories, 'is_farmer': True}
                return render(request, 'farmers/accounts/dashboard.html', context)

        # CASE B: Plain-create submission (fields: name, category, price, quantity, description, image)
        else:
            name = request.POST.get('name', '').strip()
            cat_id = request.POST.get('category')
            price_raw = request.POST.get('price')
            quantity_raw = request.POST.get('quantity')
            description = request.POST.get('description', '').strip()
            uploaded_image = request.FILES.get('image')

            # Basic validation
            if not name or not cat_id or not price_raw or not quantity_raw:
                messages.error(request, 'Please fill name, category, price and quantity.')
                context = {'form': FarmerProductForm(), 'categories': categories}
                return render(request, 'farmers/accounts/dashboard.html', context)

            # Resolve category
            try:
                category = Category.objects.get(pk=cat_id)
            except Category.DoesNotExist:
                messages.error(request, 'Selected category does not exist.')
                context = {'form': FarmerProductForm(), 'categories': categories}
                return render(request, 'farmers/accounts/dashboard.html', context)

            # Create Product (store.Product)
            try:
                price = int(float(price_raw))
            except Exception:
                # fallback to 0 if parsing fails
                price = 0
            try:
                stock = int(float(quantity_raw))
            except Exception:
                stock = 0

            # ensure slug is unique: use slugify + append counter if needed
            base_slug = slugify(name)[:240] or 'product'
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            product = Product(
                product_name=name,
                slug=slug,
                description=description,
                price=price,
                stock=stock,
                category=category,
                is_available=True
            )
            # attach uploaded image if present (field name in store.Product is 'images')
            if uploaded_image:
                product.images = uploaded_image

            product.save()

            # Create FarmerProduct linking row
            if user is None:
                messages.warning(request, 'Product created, but could not link to your farmer account. Contact admin.')
                return redirect('farmer_dashboard')

            # The FarmerProduct price is set to same as product.price by default
            fp, created = FarmerProduct.objects.get_or_create(
                farmer=user,
                product=product,
                defaults={'price': product.price, 'stock': product.stock, 'image': uploaded_image, 'is_active': True}
            )
            if not created:
                # if somehow exists, update
                fp.price = product.price
                fp.stock = product.stock
                if uploaded_image:
                    fp.image = uploaded_image
                fp.is_active = True
                fp.save()

            messages.success(request, 'Product created and added to your offerings.')
            return redirect('farmer_dashboard')

    # GET: render dashboard/add-product page with form and categories
    form = FarmerProductForm()
    context = {'form': form, 'categories': categories}
    return render(request, 'farmers/accounts/dashboard.html', context)
