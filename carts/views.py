from django.shortcuts import render,redirect,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product
from .models import Cart,CartItem
from django.contrib.auth.decorators import login_required





def _cart_id(req):
    cart = req.session.session_key
    if not cart:
        cart = req.session.create()
    return cart


def add_cart(req,product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(req))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(req)
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product,cart = cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
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



def cart(req, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if req.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=req.user, is_active = True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(req))
            cart_items = CartItem.objects.filter(cart=cart, is_active = True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context={
        'total':total,
        'quantity':quantity,
        'cart_itmes' : cart_items,
        'tax':tax,
        'grand_total': grand_total,
    }
    return render(req,'store/cart.html', context)




@login_required(login_url='login')
def checkout(req,total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if req.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=req.user, is_active = True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(req))
            cart_items = CartItem.objects.filter(cart=cart, is_active = True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context={
        'total':total,
        'quantity':quantity,
        'cart_itmes' : cart_items,
        'tax':tax,
        'grand_total': grand_total,
    }
    return render(req,'store/checkout.html',context)