from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DeleteView
from hitcount.views import HitCountDetailView
from django.contrib.auth.decorators import login_required

from shop.forms import AddQuantityForm
from .models import *


class HomeLists(ListView):
    model = Books
    template_name = 'shop/list_items.html'

    # context_object_name = 'books'             object_list -default
    # фільтр для показу книг
    def get_queryset(self):
        return Books.objects.filter(is_availible=True)  # .select_related('category')


class BookDetail(HitCountDetailView):
    model = Books
    # pk_url_kwarg = 'book_id'  default = pk
    count_hit = True


@login_required(login_url=reverse_lazy('login'))
def cart_view(request):
    cart = Order.get_cart(request.user)
    items = cart.orderitem_set.all()
    context = {
        'cart': cart,
        'items': items,
    }
    return render(request, 'shop/cart.html', context)

@login_required(login_url=reverse_lazy('login'))
def add_item_to_cart(request, pk):
    if request.method == 'POST':
        quantity_form = AddQuantityForm(request.POST)
        if quantity_form.is_valid():
            quantity = quantity_form.cleaned_data['quantity']
            if quantity:
                cart = Order.get_cart(request.user)
                # product = Product.objects.get(pk=pk)
                product = get_object_or_404(Books, pk=pk)
                cart.orderitem_set.create(product=product,
                                          quantity=quantity,
                                          price=product.price)
                cart.save()
                return redirect('cart_url')
        else:
            pass
    return redirect('list_items')

@method_decorator(login_required, name='dispatch')
class CartDeleteItem(DeleteView):
    model = OrderItem
    template_name = 'shop/cart.html'
    success_url = reverse_lazy('cart_view')

    # Проверка доступа
    def get_queryset(self):
        qs = super().get_queryset()
        qs.filter(order__user=self.request.user)
        return qs