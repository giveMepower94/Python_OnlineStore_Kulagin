from django.views.generic import ListView, DetailView, FormView
from .models import Product, Stock, Cart
from django.urls import reverse_lazy
from .forms import CartForm


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


class AddToCartView(FormView):
    form_class = CartForm
    template_name = 'store/add_to_cart.html'
    success_url = reverse_lazy('cart_detail')

    def form_valid(self, form):
        product = form.cleaned_data['product']
        quantity = form.cleaned_data['quantity']

        cart, created = Cart.objects.get_or_create(customer=self.request.user.customer)
        cart.add_item(product, quantity)
        return super().form_valid(form)


class CartDetailView(DetailView):
    model = Cart
    template_name = 'store/cart_detail.html'

    def get_object(self):
        return Cart.objects.get_or_create(customer=self.request.user.customer)

