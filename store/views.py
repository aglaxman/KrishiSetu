from django.shortcuts import render,get_object_or_404,HttpResponse
from .models import Product
from category.models import Category
from carts.models import *
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger , Paginator
# Create your views here.




def store(req, category_slug = None):
    categories = None
    products = None
    

    if category_slug != None:
        categories = get_object_or_404(Category , slug = category_slug)
        products = Product.objects.filter(category = categories , is_available = True)
        paginator = Paginator(products, 9)
        page = req.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    else:
        products = Product.objects.all().filter(is_available = True).order_by('id')
        paginator = Paginator(products, 9)
        page = req.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    
    context = {
        'products' : paged_products,
        'product_count' : product_count,
    }
    return render(req,'store/store.html',context)





def product_detail(req, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug = category_slug , slug = product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id =_cart_id(req),product = single_product).exists()
        
    except Exception as e:
        raise e
    
    context = {
        'single_product' : single_product,
        'in_cart' : in_cart,
    }
    return render(req, 'store/product_detail.html', context)