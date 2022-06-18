from django.shortcuts import render
from django.views.generic import ListView
from hitcount.views import HitCountDetailView

from .models import Books


class HomeLists(ListView):
    model = Books
    template_name = 'shop/list_items.html'
    # context_object_name = 'books'             object_list -default
    # фільтр для показу книг
    def get_queryset(self):
        return Books.objects.filter(is_availible=True) #.select_related('category')


class BookDetail(HitCountDetailView):
    model = Books
    # pk_url_kwarg = 'book_id'  default = pk
    count_hit = True