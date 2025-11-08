from django.urls import path
from .views import (ProductListView,
                    ProductDetailView,
                    StockListView,
                    StockDetailView,
                    AddToCartView,
                    CartDetailView)


urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('stock/', StockListView.as_view(), name='stock_list'),
    path('stock/<int:pk>/', StockDetailView.as_view(), name='stock_detail'),
    path('cart/add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', CartDetailView.as_view(), name='cart_detail'),
]
