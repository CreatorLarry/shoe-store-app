"""
URL configuration for shoe_store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from main import views
from shoe_store import settings

urlpatterns = [
                  path('', views.home, name='home'),

                  path('category/<str:category_slug>/', views.category_view, name='category-view'),

                  path('subcategory/<int:subcategory_id>/', views.subcategory_view, name='subcategory-view'),

                  path('product-page', views.product_page, name='product_page'),

                  path('product/<int:pk>/', views.product_details, name='product-details'),

                  path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

                  path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),

                  path('cart/', views.view_cart, name='view_cart'),

                  path('update-cart/<int:product_id>/', views.update_cart, name='update_cart'),

                  path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),

                  path('checkout/', views.checkout, name='checkout'),

                  path('checkout/confirmation/', views.checkout_confirmation_view, name='checkout_confirmation'),

                  path('thank-you/', views.thank_you, name='thank_you'),

                  path('admin/', admin.site.urls),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
