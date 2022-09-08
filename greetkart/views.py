from itertools import product
from unicodedata import category
from django.shortcuts import render
from store.models import Product
from category.models import Category

def home(request):
    products = Product.objects.all().filter(is_available=True)
    categories = Category.objects.all()
    print('h')
    print(categories)
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'home.html', context)


