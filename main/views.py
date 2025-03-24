from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')


def product_page(request):
    return render(request, 'product_page.html')


def product_details(request):
    return render(request, 'product_details.html')


def cart_page(request):
    return render(request, 'cart_page.html')


def checkout(request):
    return render(request, 'checkout.html')