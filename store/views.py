from django.views.generic import ListView, DetailView, FormView
from .models import Product, Stock, Cart, Order, OrderItem
from django.urls import reverse_lazy
from .forms import CartForm, OrderForm


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


class CreateOrderView(FormView):
    template_name = 'order_create.html'
    form_class = OrderForm
    success_url = reverse_lazy('order_success')

    def form_valid(self, form):
        user = self.request.user
        cart = user.cart

        # создаём заказ
        order = Order.objects.create(
            customer=user.customer,
            status='pending',
            total_price=0
        )

        total = 0

        # переносим товары из корзины в заказ
        for cart_item in cart.items.all():
            item_total = cart_item.product.price * cart_item.quantity
            total += item_total

            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )

        order.total_price = total
        order.save(update_fields=['total_price'])

        cart.items.all().delete()

        return super().form_valid(form)

