from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product,Variation
from .models import Cart,CartItem
from django.contrib.auth.decorators import login_required



def _cart_id(req):
    cart = req.session.session_key
    if not cart:
        cart = req.session.create()
    return cart





def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id) #get the product
    # If the user is authenticated
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass


        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')
    # If the user is not authenticated
    else:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass


        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            # existing_variations -> database
            # current variation -> product_variation
            # item_id -> database
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            print(ex_var_list)

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')


def remove_cart(req, product_id,cart_item_id):
    product = get_object_or_404(Product, id =  product_id)
    try:
        if req.user.is_authenticated:
            cart_item = CartItem.objects.get(product = product , user = req.user , id =cart_item_id)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(req))
            cart_item = CartItem.objects.get(product = product , cart = cart  ,id=cart_item_id)
        if(cart_item.quantity > 1):
            cart_item.quantity -= 1 
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def remove_cart_item(req , product_id , cart_item_id):
    product = get_object_or_404(Product,id = product_id)
    if req.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product , user=req.user ,  id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id = _cart_id(req))
        cart_item = CartItem.objects.get(product=product , cart=cart)
    cart_item.delete()
    return redirect('cart')



import logging
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)

def cart(req):
    total = 0.0
    quantity = 0
    tax = 0.0
    grand_total = 0.0
    cart_items = []

    try:
        # Get cart items for logged-in user
        if req.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=req.user, is_active=True)
        else:
            # Use filter() instead of get() to avoid DoesNotExist being raised
            cart_qs = Cart.objects.filter(cart_id=_cart_id(req))
            cart = cart_qs.first()  # None if not found
            if cart:
                cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            else:
                cart_items = []

        # Defensive iteration: if sub_total fails, fallback to price*quantity
        for cart_item in cart_items:
            try:
                # prefer the model's sub_total method (which should include weight/unit & qty)
                item_total = float(cart_item.sub_total())
            except Exception as e:
                # log the error and fallback
                logger.exception("CartItem.sub_total() failed for CartItem id=%s. Falling back to price*quantity.", getattr(cart_item, 'id', 'unknown'))
                try:
                    item_total = float(cart_item.product.price) * int(cart_item.quantity)
                except Exception:
                    # worst-case fallback to 0
                    item_total = 0.0

            total += item_total
            # keep overall quantity as sum of quantities (for UI counters)
            try:
                quantity += int(cart_item.quantity)
            except Exception:
                quantity += 0

        tax = (2.0 * total) / 100.0  # 2%
        grand_total = total + tax

    except Exception as e:
        # Catch-all so we can log unexpected issues — do not crash the page
        logger.exception("Unexpected error in cart view: %s", e)
        total = 0.0
        quantity = 0
        tax = 0.0
        grand_total = 0.0
        cart_items = []

    # Provide both names in context in case template still uses the old typo
    context = {
        'total': round(total, 2),
        'quantity': quantity,
        'cart_items': cart_items,
        'cart_itmes': cart_items,     # keep old name for compatibility (remove later)
        'tax': round(tax, 2),
        'grand_total': round(grand_total, 2),
    }

    return render(req, 'store/cart.html', context)





import logging
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)

@login_required(login_url='login')
def checkout(req):
    total = 0.0
    quantity = 0
    tax = 0.0
    grand_total = 0.0
    cart_items = []

    try:
        # For a logged-in user (login_required ensures user is authenticated),
        # but keep guest/fallback logic safe in case you remove the decorator later.
        if req.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=req.user, is_active=True)
        else:
            cart_qs = Cart.objects.filter(cart_id=_cart_id(req))
            cart = cart_qs.first()
            if cart:
                cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            else:
                cart_items = []

        # Calculate totals using the model's sub_total (weight/unit aware)
        for cart_item in cart_items:
            try:
                item_total = float(cart_item.sub_total())
            except Exception:
                logger.exception(
                    "checkout: failed to compute sub_total for CartItem id=%s. Falling back to price*quantity.",
                    getattr(cart_item, 'id', 'unknown')
                )
                try:
                    item_total = float(cart_item.product.price) * int(cart_item.quantity)
                except Exception:
                    item_total = 0.0

            total += item_total

            try:
                quantity += int(cart_item.quantity)
            except Exception:
                quantity += 0

        tax = (2.0 * total) / 100.0
        grand_total = total + tax

    except Exception as e:
        logger.exception("Unexpected error in checkout view: %s", e)
        total = 0.0
        quantity = 0
        tax = 0.0
        grand_total = 0.0
        cart_items = []

    context = {
        'total': round(total, 2),
        'quantity': quantity,
        'cart_items': cart_items,
        'cart_itmes': cart_items,   # kept for backward compatibility with template typo
        'tax': round(tax, 2),
        'grand_total': round(grand_total, 2),
    }

    return render(req, 'store/checkout.html', context)
