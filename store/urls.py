from django.urls import path
from .views import (ProductListView, 
                    ProductDetailView,
                    StockListView,
                    StockDetailView)


urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('stock/', StockListView.as_view(), name='stock_list'),
]
