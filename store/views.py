from django.views.generic import ListView, DetailView, FormView
from .models import Product, Stock, Cart, Order, OrderItem
from django.urls import reverse_lazy
from .forms import CartForm, OrderForm
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'

    # перенаправление неавторизованных на страницу логина
    login_url = '/users/login/'
    redirect_field_name = 'next'


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'
    login_url = '/users/login/'


class StockListView(LoginRequiredMixin, ListView):
    model = Stock
    template_name = 'store/stock_list'
    context_object_name = 'stocks'
    login_url = '/users/login/'

    def get_queryset(self):
        return Stock.objects.all()


class StockDetailView(LoginRequiredMixin, DetailView):
    model = Stock
    template_name = 'store/stock_detail'
    context_object_name = 'stock'
    login_url = '/users/login/'


class AddToCartView(LoginRequiredMixin, FormView):
    form_class = CartForm
    template_name = 'store/add_to_cart.html'
    success_url = reverse_lazy('cart_detail')
    login_url = '/users/login/'

    def form_valid(self, form):
        product = form.cleaned_data['product']
        quantity = form.cleaned_data['quantity']

        cart, created = Cart.objects.get_or_create(customer=self.request.user.customer)
        cart.add_item(product, quantity)
        return super().form_valid(form)


class CartDetailView(LoginRequiredMixin, DetailView):
    model = Cart
    template_name = 'store/cart_detail.html'
    login_url = '/users/login/'

    def get_object(self):
        return Cart.objects.get_or_create(customer=self.request.user.customer)


class CreateOrderView(LoginRequiredMixin, FormView):
    template_name = 'store/order_create.html'
    form_class = OrderForm
    success_url = reverse_lazy('order_success')
    login_url = '/users/login/'

    def form_valid(self, form):
        user = self.request.user
        cart = user.customer.cart

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

        return render(self.request, 'store/order_success.html', {'order': order})


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'store/order_detail.html'
    context_object_name = 'order'
    login_url = '/users/login/'

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user.customer)
