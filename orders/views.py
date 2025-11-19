from django.shortcuts import render,HttpResponse,redirect
from carts.models import CartItem
from .forms import OrderForm
from .models import Order,OrderProduct
import datetime
import logging
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
logger = logging.getLogger(__name__)
# Create your views here.



def payments(req):
    return render(req,'orders/payments.html')




from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages

def place_order(request):
    
    current_user = request.user

    # If the cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    total = 0.0
    quantity = 0.0
    tax = 0.0
    grand_total = 0.0
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
        try:
            quantity += int(cart_item.quantity)
        except Exception:
            quantity += 0

    tax = (2.0 * total) / 100.0  # 2%
    grand_total = total + tax
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all the billing information inside Order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payments.html', context)
        else:
            return HttpResponse('failed')
    else:
        return redirect('checkout')