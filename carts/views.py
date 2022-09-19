from itertools import product
from urllib import request
from django.shortcuts import render, redirect
from store.models import Product, Variation
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
# Create your views here.


def _cart_id(request):
    cart = request.session.session_key

    if not cart:
        cart = request.session.create()

    return cart


def cart(request, total=0, qty=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.qty)
            qty = cart_item.qty
        tax = (2 * total/100)
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'qty': qty,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,

    }
    return render(request, 'store/cart.html', context)


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    products_variation = []
    if request.method == "POST":
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                variation = Variation.objects.get(
                    product=product, variation_category=key, variation_value=value)
                products_variation.append(variation)

            except:
                pass
    try:
        # Get the cart using the cart_id preset in the session
        cart = Cart.objects.get(cart_id=_cart_id(request))

    except ObjectDoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
        cart.save()

    try:
        products_variation_lenght = len(products_variation)


        #Checking if the variation in already exist
        try:
            print("Checking if the variasion in sart is exist")
            print(f"key: {key} value: {value}")
            print(f"product: {product}")
            this_item = CartItem.objects.filter(product=product, variations__variation_category=key, variations__variation_value = value)
            print(f"this item: {this_item}")
            if this_item:
                print("yes")
                this_item = this_item.first()
                this_item.qty += 1
                this_item.save()
            else:
                print("no")

                cart_item = CartItem.objects.create(product=product, cart=cart, qty=1)

                
                if products_variation_lenght > 0:
                    cart_item.variations.clear()
                    for item in products_variation:
                        cart_item.variations.add(item)
                # cart_item.qty += 1
                cart_item.save()
        except:
            print("now working")

    except ObjectDoesNotExist:
        print("CCC")
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            qty=1,
        )

        if len(products_variation) > 0:
            cart_item.variations.clear()
            for item in products_variation:
                print("h")
                cart_item.variations.add(item)
                cart_item.save()

    return redirect('cart')


def remove_qty(request, cartitem_id):
    # print("in remove")
    # product = Product.objects.get(id=product_id)
    # try:
    #     # Get the cart using the cart_id preset in the session
    #     cart = Cart.objects.get(cart_id=_cart_id(request))

    # except Cart.DoesNotExist:
    #     pass

    # try:
    #     cart_item = CartItem.objects.get(product=product, cart=cart)
    #     if cart_item.qty <= 0:
    #         pass
    #     else:
    #         cart_item.qty -= 1
    #         cart_item.save()

    # except CartItem.DoesNotExist:
    #     pass

    cart_item = CartItem.objects.get(pk=cartitem_id)
    if cart_item.qty <= 0:
        pass
    else:
        cart_item.qty -= 1
        cart_item.save()


    return redirect('cart')

def add_cart_qty(request, cartitem_id):

    cart_item = CartItem.objects.get(pk=cartitem_id)

    cart_item.qty += 1
    cart_item.save()


    return redirect('cart')


def remove_cart_qty(request, cartitem_id):
    # print("in remove")
    # product = Product.objects.get(id=product_id)
    # try:
    #     # Get the cart using the cart_id preset in the session
    #     cart = Cart.objects.get(cart_id=_cart_id(request))

    # except ObjectDoesNotExist:
    #     pass

    # try:
    #     cart_item = CartItem.objects.get(product=product, cart=cart)
    #     cart_item.delete()
    # except ObjectDoesNotExist:
    #     pass

    cart_item = CartItem.objects.get(pk=cartitem_id)
    cart_item.delete()


    return redirect('cart')
