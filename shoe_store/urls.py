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

from django.contrib.auth.views import LogoutView

urlpatterns = [
                  path('', views.home, name='home'),

                  path('category/<str:category_slug>/', views.category_view, name='category-view'),

                  path('subcategory/<int:subcategory_id>/', views.subcategory_view, name='subcategory-view'),

                  path('product-page/', views.product_page, name='product_page'),

                  path('product/<int:pk>/', views.product_details, name='product-details'),

                  path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

                  path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),

                  path('cart/', views.view_cart, name='view_cart'),

                  path('update-cart/<int:product_id>/', views.update_cart, name='update_cart'),

                  path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),

                  path('checkout/', views.checkout, name='checkout'),

                  path('checkout/confirmation/', views.checkout_confirmation_view, name='checkout_confirmation'),

                  path('thank-you/', views.thank_you, name='thank_you'),

                  path('pay-for-product/<int:order_id>/', views.pay_for_product, name='pay_for_product'),

                  path('handle/response/transaction/', views.callback, name='mpesa_callback'),

                  path('dashboard/', views.vendor_dashboard_home, name='vendor_dashboard_home'),

                  path('login/', views.vendor_login, name='login'),

                #   path('logout/', LogoutView.as_view(next_page='login'), name='logout'), 
                  path('logout/', views.logout_page, name='logout_page'),
                
                  path('register/', views.vendor_register, name='register'),
                  
                  path('profile/', views.vendor_profile, name='vendor_profile'),
                  
                  path('update-profile/', views.update_profile, name='update_profile'),

                  path('add-product/', views.add_product, name='add_product'),
                  
                  path('update-product/<int:pk>/', views.update_product, name='update_product'),
                  
                  path('delete-product/<int:pk>/', views.delete_product, name='delete_product'),

                  path('product-list/', views.product_list, name='product_list'),
                  
                  path('charts/', views.charts_view, name='charts'),
                  
                  path('charts/area-data/', views.area_chart_data, name='area_chart_data'),
                  
                  path('charts/bar-data/', views.bar_chart_data, name='bar_chart_data'),
                  
                  path('charts/pie-data/', views.pie_chart_data, name='pie_chart_data'),


                  path('admin/', admin.site.urls),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
