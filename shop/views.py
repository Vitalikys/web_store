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
    my_balance  = Payment.get_balance(request.user)
    cart = Order.get_cart(request.user)
    items = cart.orderitem_set.all()
    context = {
        'my_balance':my_balance,
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
                return redirect('list_items')
        else:
            pass
    return redirect('list_items')

# DoesNotExist at /delete_item/9  #ERROR Order matching query does not exist.
@method_decorator(login_required, name='dispatch')
class CartDeleteItem(DeleteView):
    model = OrderItem
    template_name = 'shop/cart.html'
    success_url = reverse_lazy('cart_url')

    # Проверка доступа
    def get_queryset(self):
        qs = super().get_queryset()
        qs.filter(order__user=self.request.user)
        return qs

# спроба №2  . не працює    type object 'OrderItem' has no attribute 'object'
# def cart_remove(request, pk):
#     cart = OrderItem(request)
#     book = get_object_or_404(Books, id=pk)
#     cart.remove(book)
#     return redirect('cart_url')
def cart_remove(request, pk):
    order = OrderItem.objects.get(id=pk)
    order.delete()
    return redirect('cart_url')

@login_required(login_url=reverse_lazy('login'))
def make_order(request):
    cart = Order.get_cart(request.user)
    cart.make_order()
    return redirect('cart_url')

def about(request):
    return render(request, 'shop/about.html')