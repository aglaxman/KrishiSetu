# carts/context_processors.py
from .views import _cart_id
from .models import Cart, CartItem
from django.conf import settings

def counter(request):
    """
    Returns count of items in cart for the template.
    Works for authenticated users (CartItem.user FK) and anonymous users (session cart_id).
    """
    cart_count = 0

    # If user is authenticated, count cart items linked to the user
    if getattr(request, "user", None) and request.user.is_authenticated:
        try:
            # ensure request.user is actually a User model instance
            # (defensive: if request.user is not an instance, this will raise and go to except)
            cart_items = CartItem.objects.filter(user=request.user)
            cart_count = cart_items.count()
        except Exception:
            # If anything unexpected happens, don't crash page rendering.
            cart_count = 0

    else:
        # anonymous user: use session-based cart id
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart)
            cart_count = cart_items.count()
        except Cart.DoesNotExist:
            cart_count = 0
        except Exception:
            # Catch other unexpected problems gracefully
            cart_count = 0

    return {'cart_count': cart_count}
