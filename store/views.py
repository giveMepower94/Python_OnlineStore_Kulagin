from django.views.generic import ListView, DetailView
from .models import Product, Stock


# Create your views here.
class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'


class StockListView(ListView):
    model = Stock
    template_name = 'store/stock_list'
    context_object_name = 'stocks'
    
    def get_queryset(self):
        return Stock.objects.all()


class StockDetailView(DetailView):
    model = Stock
    template_name = 'store/stock_detail'
    context_object_name = 'stock'
