from django.shortcuts import render, get_object_or_404, redirect

from main.models import Product, Category, Size


# Create your views here.
def home(request):
    products = Product.objects.all()
    new_arrivals = Product.objects.order_by('-created_at')[:2]
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


def view_cart(request):
    cart_items = request.session.get('cart', [])

    # Optional: convert product IDs into actual Product objects
    items = []
    for item in cart_items:
        try:
            product = Product.objects.get(id=item['product_id'])
            items.append({
                'product': product,
                'quantity': item['quantity'],
            })
        except Product.DoesNotExist:
            continue

    total = sum(i['product'].price * i['quantity'] for i in items)

    return render(request, 'cart_page.html', {
        'cart_items': items,
        'total': total,
    })


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


def category_view(request, category_slug):
    # Optional: filter using Category model if you have it
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category__slug=category_slug)

    return render(request, 'category.html', {
        'products': products,
        'category': category,
        'category_name': category_slug.capitalize(),  # Optional for display
    })


def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Handle purchase logic here...
    return render(request, 'checkout.html', {'product': product})
