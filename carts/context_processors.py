from .models import Cart,CartItem
from .views import _cart_id

def counter(req):
    cart_count = 0
    if ('admin' in req.path):
        return()
    else:
        try:
            cart = Cart.objects.filter(cart_id = _cart_id(req))
            cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except cart.DoesNotExist : 
            cart_count = 0
    return dict(cart_count = cart_count)