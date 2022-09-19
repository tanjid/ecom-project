from ast import keyword
from django.http import HttpResponse
from multiprocessing import context
from unicodedata import category
from django.shortcuts import render, get_object_or_404
from store.models import Product
from category.models import Category
from carts.models import CartItem
from django.core.exceptions import ObjectDoesNotExist
from carts.views import _cart_id
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.

def store(request, category_slug=None,):
    categories = None
    products = None
    
    if category_slug:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        products_count = products.count()

    else:
        products = Product.objects.all().filter(is_available=True)
        products_count = products.count()

    paginator = Paginator(products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(number=page_number)
    context = {
        'products': products,
        'products_count': products_count,
        'page_obj': page_obj,
    }
    return render(request, 'store/store.html', context)

def single_product(request, category_slug, product_slug):
    try:
        selected_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        already_in_cart_check = CartItem.objects.filter(cart__cart_id= _cart_id(request), product = selected_product).exists()
    except Exception as e:
        raise e
    
    
    context = {
        'selected_product': selected_product,
        'already_in_cart_check': already_in_cart_check
    }
    return render(request, 'store/single_product.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']

        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            products_count = products.count()
            print(products)
            context = {
                'page_obj': products,
                'products_count': products_count
            }
            return render(request, 'store/store.html', context)
    return render(request, 'store/store.html')