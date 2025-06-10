import json

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django_daraja.mpesa.core import MpesaClient

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import VendorRegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from main.models import Product, Category, Size, Order, Banner, SubCategory, MpesaTransaction, OrderItem, Color


# Create your views here.
def home(request):
    products = Product.objects.all()
    new_arrivals = Product.objects.filter(is_new=True).order_by('-created_at')[:8]
    categories = Category.objects.all()
    banners = Banner.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'home.html',
                  {'products': products, 'new_arrivals': new_arrivals, 'categories': categories, 'banners': banners})


def product_page(request):
    selected_category = request.GET.get('category')
    selected_subcategories = request.GET.getlist('subcategory')
    sort_option = request.GET.get('sort', 'default')
    page_number = request.GET.get('page', 1)

    if selected_category:
        try:
            category = Category.objects.get(id=selected_category)
            return redirect(reverse('category-view', args=[category.slug]))
        except Category.DoesNotExist:
            pass  # fallback to general page

    products = Product.objects.all()

    if selected_subcategories:
        try:
            subcategory = SubCategory.objects.get(id=selected_subcategories[0])
            return redirect(reverse('subcategory-view', args=[subcategory.id]))
        except (SubCategory.DoesNotExist, IndexError):
            pass  # If invalid or empty list

    # Sorting logic
    if sort_option == 'price-low':
        products = products.order_by('price')
    elif sort_option == 'price-high':
        products = products.order_by('-price')
    elif sort_option == 'new':
        products = products.order_by('-created_at')

    # 🔽 Paginate - 15 products per page
    paginator = Paginator(products, 15)
    paginated_products = paginator.get_page(page_number)

    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()

    context = {
        'products': paginated_products,  # now paginated
        'categories': categories,
        'subcategories': subcategories,
        'selected_category': selected_category,
        'selected_subcategories': selected_subcategories,
        'selected_sort': sort_option,
        'paginator': paginator,
        'page_obj': paginated_products,
    }
    return render(request, 'product_page.html', context)


def product_details(request, pk):
    product = get_object_or_404(Product, pk=pk)
    sizes = Size.objects.all()
    colors = product.colors.all()
    suggested_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    return render(request, 'product_details.html',
                  {'product': product, 'sizes': sizes, 'colors': colors, 'suggested_products': suggested_products})


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
        messages.success(request, 'Successfully added to cart.')
        return redirect('view_cart')


def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', [])
        cart = [item for item in cart if item['product_id'] != product_id]
        request.session['cart'] = cart
        return JsonResponse({'success': True})

    messages.success(request, 'Removed from cart.')
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
    messages.success(request, 'Cart Updated.')
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def category_view(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    selected_subcategories = request.GET.getlist('subcategory')
    sort_option = request.GET.get('sort', 'default')
    page_number = request.GET.get('page', 1)

    products = Product.objects.filter(category=category)

    # If filtering by subcategories
    if selected_subcategories:
        products = products.filter(subcategory__id__in=selected_subcategories)

    # Sorting logic
    if sort_option == 'price-low':
        products = products.order_by('price')
    elif sort_option == 'price-high':
        products = products.order_by('-price')
    elif sort_option == 'new':
        products = products.order_by('-created_at')

    # Pagination
    paginator = Paginator(products, 15)
    paginated_products = paginator.get_page(page_number)

    categories = Category.objects.all()
    subcategories = SubCategory.objects.filter(category=category)  # optional: filter subs by this category only

    context = {
        'category': category,
        'products': paginated_products,
        'categories': categories,
        'subcategories': subcategories,
        'selected_category': category.id,
        'selected_subcategories': selected_subcategories,
        'selected_sort': sort_option,
        'paginator': paginator,
        'page_obj': paginated_products,
    }
    return render(request, 'category.html', context)


def subcategory_view(request, subcategory_id):
    sort_option = request.GET.get('sort', 'default')

    try:
        subcategory = SubCategory.objects.get(id=subcategory_id)
    except SubCategory.DoesNotExist:
        return redirect('product-page')  # Or show a 404

    products = Product.objects.filter(subcategory=subcategory)

    if sort_option == 'price-low':
        products = products.order_by('price')
    elif sort_option == 'price-high':
        products = products.order_by('-price')
    elif sort_option == 'new':
        products = products.order_by('-created_at')

    paginator = Paginator(products, 15)
    page_number = request.GET.get('page', 1)
    paginated_products = paginator.get_page(page_number)

    context = {
        'subcategory': subcategory,  # Make sure this is passed
        'products': paginated_products,
        'selected_sort': sort_option,
        'page_obj': paginated_products,
    }
    return render(request, 'subcategory.html', context)


def checkout(request):
    cart = request.session.get('cart', [])

    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('view_cart')

    total = sum(item['price'] * item['quantity'] for item in cart)
    source = request.GET.get('source')

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
        'source': source,
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
            return redirect('product_details', product_id=product_id)

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

        # Save to session for use in confirmation
        request.session['buy_now'] = [{
            'product_id': product.id,
            'product_title': product.title,
            'price': float(product.price),
            'quantity': quantity,
            'size': size_name,
            'color': color,
            'total': float(total)
        }]
        messages.success(request, 'Proceeding to checkout for 1 item.')
        return render(request, 'checkout.html', {
            'cart_items': [{
                'product': product,
                'quantity': quantity,
                'total': total,
                'size': size_name,
                'color': color
            }],
            'total': total,
            'source': 'buy_now'
        })

    return redirect('product-details', pk=product_id)


def checkout_confirmation_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        # Save this info in session
        checkout_data = {
            'name': name,
            'email': email,
            'phone': phone,
            'address': address,
            'payment_method': payment_method
        }
        request.session['checkout_data'] = checkout_data

        return redirect('checkout_confirmation')

    # GET request
    checkout_data = request.session.get('checkout_data')
    cart = request.session.get('cart', [])
    buy_now_data = request.session.get('buy_now')

    if not checkout_data:
        return redirect('checkout')

    cart_items = []
    total = 0

    if cart:
        for item in cart:
            try:
                product = Product.objects.get(id=item['product_id'])
                item_total = float(item['price']) * item['quantity']
                total += item_total
                cart_items.append({
                    'product': product,
                    'size': item['size'],
                    'color': item['color'],
                    'quantity': item['quantity'],
                    'price': item['price'],
                    'total': item_total
                })
            except Product.DoesNotExist:
                continue

    elif buy_now_data:
        for item in buy_now_data:
            try:
                product = Product.objects.get(id=item['product_id'])
                total += item['total']
                cart_items.append({
                    'product': product,
                    'size': item['size'],
                    'color': item['color'],
                    'quantity': item['quantity'],
                    'price': item['price'],
                    'total': item['total']
                })
            except Product.DoesNotExist:
                continue

    # ✅ CREATE ORDER if not created yet
    order_id = request.session.get('latest_order_id')
    order = None

    if not order_id:
        order = Order.objects.create(
            name=checkout_data['name'],
            email=checkout_data['email'],
            phone=checkout_data['phone'],
            address=checkout_data['address'],
            payment_method=checkout_data['payment_method'],
            total=total
        )

        # Save each order item
        for item in cart_items:
            # Get Size instance
            try:
                size_instance = Size.objects.get(name=item['size'])
            except Size.DoesNotExist:
                size_instance = None  # Optional: Handle missing size more gracefully

            # Create OrderItem (without colors yet)
            order_item = OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                size=size_instance,
                price=item['price']
            )

            # Handle ManyToManyField: colors
            color_data = item.get('color')
            if color_data:
                if isinstance(color_data, list):
                    color_qs = Color.objects.filter(name__in=color_data)
                else:
                    color_qs = Color.objects.filter(name=color_data)
                order_item.colors.set(color_qs)

        # Store order ID in session
        request.session['latest_order_id'] = order.id

    else:
        order = Order.objects.get(id=order_id)

    messages.success(request, 'Details confirmed. Proceed to finalize your payment.')

    return render(request, 'checkout_confirmation.html', {
        'checkout_data': checkout_data,
        'cart_items': cart_items,
        'total': total,
        'order': order  # ✅ Now order is available in template
    })


def pay_for_product(request, order_id):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        total = request.POST.get('amount')

        try:
            order = Order.objects.get(order_id=order_id)
        except Order.DoesNotExist:
            return redirect('checkout_confirmation')  # Or a 404 page

        cl = MpesaClient()

        phone_number = phone
        if total is None:
            messages.error(request, "Payment amount is missing.")
            return redirect('checkout_confirmation')

        try:
            amount = float(total)
        except (TypeError, ValueError):
            messages.error(request, "Invalid amount format.")
            return redirect('checkout_confirmation')

        account_reference = f"Order-{order.id}"
        transaction_desc = f"Payment for Order #{order.id}"
        callback_url = 'https://lively-prime-chow.ngrok-free.app/handle/response/transaction/'

        response = cl.stk_push(
            phone_number, amount, account_reference, transaction_desc, callback_url
        )

        # You can optionally store merchant_request_id and checkout_request_id temporarily here
        if response.response_code == "0":
            # Successful initiation
            # You might want to save something to track this transaction before callback
            pass

        return redirect('checkout_confirmation')


def callback(request):
    data = json.loads(request.body)

    try:
        stk_callback = data['Body']['stkCallback']
        merchant_request_id = stk_callback['MerchantRequestID']
        checkout_request_id = stk_callback['CheckoutRequestID']
        result_code = stk_callback['ResultCode']
        result_desc = stk_callback['ResultDesc']

        if result_code == 0:
            # Successful transaction
            metadata = stk_callback['CallbackMetadata']['Item']
            mpesa_receipt_number = next(item['Value'] for item in metadata if item['Name'] == 'MpesaReceiptNumber')
            phone_number = next(item['Value'] for item in metadata if item['Name'] == 'PhoneNumber')
            amount = next(item['Value'] for item in metadata if item['Name'] == 'Amount')
            transaction_date_raw = next(item['Value'] for item in metadata if item['Name'] == 'TransactionDate')

            # Format the transaction date
            from datetime import datetime
            transaction_date = datetime.strptime(str(transaction_date_raw), "%Y%m%d%H%M%S")

            # Save transaction
            MpesaTransaction.objects.create(
                phone_number=phone_number,
                mpesa_receipt_number=mpesa_receipt_number,
                amount=amount,
                transaction_date=transaction_date,
                merchant_request_id=merchant_request_id,
                checkout_request_id=checkout_request_id,
                result_code=result_code,
                result_desc=result_desc,
            )

    except Exception as e:
        print("Callback processing error:", e)

    return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})


def thank_you(request):
    checkout_data = request.session.get('checkout_data')
    cart = request.session.get('cart', [])
    buy_now_data = request.session.get('buy_now')

    if not checkout_data:
        return redirect('checkout')

    cart_items = []

    if cart:
        # Use cart if it has items
        for item in cart:
            try:
                product = Product.objects.get(id=item['product_id'])
                cart_items.append({
                    'product': product,
                    'size': item['size'],
                    'color': item['color'],
                    'quantity': item['quantity'],
                    'price': item['price'],
                    'total': float(item['price']) * item['quantity']
                })
            except Product.DoesNotExist:
                continue
    elif buy_now_data:
        # Fallback to buy now
        for item in buy_now_data:
            try:
                product = Product.objects.get(id=item['product_id'])
                cart_items.append({
                    'product': product,
                    'size': item['size'],
                    'color': item['color'],
                    'quantity': item['quantity'],
                    'price': item['price'],
                    'total': item['total']
                })
            except Product.DoesNotExist:
                continue

    total = sum(item['total'] for item in cart_items)

    # Optional: clear session data after successful checkout
    request.session.pop('cart', None)
    request.session.pop('buy_now', None)
    request.session.pop('checkout_data', None)

    messages.success(request, 'Thank you! Your order has been received.')
    return render(request, 'thankyou_page.html', {
        'checkout_data': checkout_data,
        'cart_items': cart_items,
        'total': total
    })

# Vendor Dashboard Views

def vendor_dashboard_home(request):
    return render(request, 'vendor_dashboard_home.html')


def vendor_register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register_page')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('register_page')

        user = User.objects.create_user(
            username=email,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        messages.success(request, "Account created successfully. Please log in.")
        return redirect('login')

    return render(request, 'register_page.html') 


def vendor_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('vendor_dashboard_home')
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('login')
    return render(request, 'login_page.html')

def product_list(request):
    request(render, 'product_list.html')

def add_product(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category = Category.objects.get(id=request.POST.get('category'))
        subcategory_id = request.POST.get('subcategory')
        subcategory = SubCategory.objects.get(id=subcategory_id) if subcategory_id else None
        gender = request.POST.get('gender')
        type_ = request.POST.get('type')
        price = request.POST.get('price')
        description = request.POST.get('description')
        is_new = request.POST.get('is_new') == 'True'

        display_image = request.FILES.get('display_image')
        image_one = request.FILES.get('image_one')
        image_two = request.FILES.get('image_two')
        image_three = request.FILES.get('image_three')

        product = Product.objects.create(
            vendor=request.user,
            title=title,
            category=category,
            subcategory=subcategory,
            gender=gender,
            type=type_,
            price=price,
            description=description,
            display_image=display_image,
            image_one=image_one,
            image_two=image_two,
            image_three=image_three,
            is_new=is_new
        )

        sizes = request.POST.getlist('sizes')
        colors = request.POST.getlist('colors')

        product.sizes.set(sizes)
        product.colors.set(colors)

        return redirect('vendor_dashboard_home')  # or your desired redirect

    context = {
        'categories': Category.objects.all(),
        'subcategories': SubCategory.objects.all(),
        'sizes': Size.objects.all(),
        'colors': Color.objects.all(),
    }
    return render(request, 'add_product.html', context)


def update_product(request, product_id):
    product = Product.objects.get(id=product_id, vendor=request.user)

    if request.method == 'POST':
        product.title = request.POST.get('title')
        product.category = Category.objects.get(id=request.POST.get('category'))
        subcategory_id = request.POST.get('subcategory')
        product.subcategory = SubCategory.objects.get(id=subcategory_id) if subcategory_id else None
        product.gender = request.POST.get('gender')
        product.type = request.POST.get('type')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description')
        product.is_new = request.POST.get('is_new') == 'True'

        if 'display_image' in request.FILES:
            product.display_image = request.FILES.get('display_image')
        if 'image_one' in request.FILES:
            product.image_one = request.FILES.get('image_one')
        if 'image_two' in request.FILES:
            product.image_two = request.FILES.get('image_two')
        if 'image_three' in request.FILES:
            product.image_three = request.FILES.get('image_three')

        product.save()
        product.sizes.set(request.POST.getlist('sizes'))
        product.colors.set(request.POST.getlist('colors'))

        return redirect('vendor_dashboard')

    context = {
        'product': product,
        'categories': Category.objects.all(),
        'subcategories': SubCategory.objects.all(),
        'sizes': Size.objects.all(),
        'colors': Color.objects.all(),
    }
    return render(request, 'update_product.html', context)



