from .models import CartItem

def cart_item_count(request):
    if 'admin' in request.path:
        return {}
    else:
        cart_items = CartItem.objects.all()
        cart_items_count = 0
        for item in cart_items:
            cart_items_count  += item.qty

        return dict(cart_items_count=cart_items_count)