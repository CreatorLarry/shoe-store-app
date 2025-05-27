import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from main.models import Product, Category, Size, Order


# Create your views here.
def home(request):
    products = Product.objects.all()
    new_arrivals = Product.objects.filter(is_new=True).order_by('-created_at')[:8]
    categories = Category.objects.all()
    return render(request, 'home.html', {'products': products, 'new_arrivals': new_arrivals, 'categories': categories})


def product_page(request):
    products = Product.objects.all()
    return render(request, 'product_page.html', {'products': products})


def product_details(request, pk):
    product = get_object_or_404(Product, pk=pk)
    sizes = Size.objects.all()
    colors = product.colors.all()
    return render(request, 'product_details.html', {'product': product, 'sizes': sizes, 'colors': colors})


def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        size_id = request.POST.get('size')
        color = request.POST.get('color')
        size = get_object_or_404(Size, id=size_id)

        cart = request.session.get('cart', [])

        cart.append({
            'product_id': product.id,
            'title': product.title,
            'price': float(product.price),
            'size': size.name,
            'color': color,
            'quantity': 1,
        })

        request.session['cart'] = cart
        return redirect('view_cart')


def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', [])
        cart = [item for item in cart if item['product_id'] != product_id]
        request.session['cart'] = cart
        return JsonResponse({'success': True})

    return JsonResponse({'success': False})


def view_cart(request):
    cart = request.session.get('cart', [])
    cart_items = []

    for item in cart:
        try:
            product = Product.objects.get(id=item['product_id'])
            cart_items.append({
                'product': product,
                'size': item['size'],
                'color': item['color'],
                'quantity': item['quantity'],
                'price': item['price'],
                # 'product_id': item['product_id'],
                'total': float(item['price']) * item['quantity']
            })
        except Product.DoesNotExist:
            continue

    total = sum(item['price'] * item['quantity'] for item in cart_items)

    return render(request, 'cart_page.html', {
        'cart_items': cart_items,
        'total': total,
    })


def update_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', [])
        data = json.loads(request.body)
        action = data.get('action')

        updated = False
        for item in cart:
            if item['product_id'] == product_id:
                if action == 'increase':
                    item['quantity'] += 1
                    updated = True
                elif action == 'decrease' and item['quantity'] > 1:
                    item['quantity'] -= 1
                    updated = True
                break

        if updated:
            request.session['cart'] = cart
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'Could not update quantity.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def category_view(request, category_slug):
    # Optional: filter using Category model if you have it
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category__slug=category_slug)

    return render(request, 'category.html', {
        'products': products,
        'category': category,
        'category_name': category_slug.capitalize(),  # Optional for display
    })


def checkout(request):
    cart = request.session.get('cart', [])

    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('view_cart')

    total = sum(item['price'] * item['quantity'] for item in cart)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        # Save order to DB (for now just simulate)
        print("Order Placed:")
        print(f"Customer: {name}, Email: {email}, Phone: {phone}")
        print(f"Payment: {payment_method}, Address: {address}")
        print(f"Cart Items: {cart}")
        print(f"Total: {total}")

        # Optional: Save order to model here
        Order.objects.create(
            name=name,
            email=email,
            phone=phone,
            address=address,
            payment_method=payment_method,
            items=cart,
            total=total
        )

        # Clear cart
        request.session['cart'] = []
        messages.success(request, "Order placed successfully!")

        return redirect('product_page')  # or show a thank-you page

    # Prepare cart item structure for template
    for item in cart:
        item['total'] = item['price'] * item['quantity']
        item['product'] = get_object_or_404(Product, id=item['product_id'])

    return render(request, 'checkout.html', {
        'cart_items': cart,
        'total': total,
    })


def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        size_id = request.POST.get('size')
        color = request.POST.get('color')
        quantity = request.POST.get('quantity')

        # Convert quantity safely
        try:
            quantity = int(quantity)
            if quantity < 1:
                raise ValueError
        except (ValueError, TypeError):
            messages.error(request, 'Invalid quantity.')
            return redirect('product_detail', product_id=product_id)

        # Look up size name from ID
        size_name = None
        if size_id:
            try:
                from .models import Size  # only needed if not already imported
                size_obj = Size.objects.get(id=size_id)
                size_name = size_obj.name
            except Size.DoesNotExist:
                size_name = "Unknown"

        total = product.price * quantity

        return render(request, 'checkout.html', {
            'cart_items': [{
                'product': product,
                'quantity': quantity,
                'total': total,
                'size': size_name,  # Now the readable name
                'color': color
            }],
            'total': total,
            'source': 'buy_now'
        })

    return redirect('product-details', pk=product_id)
