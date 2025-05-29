from .models import Product  # Optional if you're not querying Product anymore

def cart_item_count(request):
    count = 0
    if 'cart' in request.session:
        cart_items = request.session.get('cart', [])
        count = sum(item.get('quantity', 1) for item in cart_items)
    return {'cart_item_count': count}
