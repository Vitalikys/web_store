from django.urls import path, include
from django.views.generic import TemplateView

from shop import views
from .views import *

urlpatterns = [
    path('', HomeLists.as_view(), name='list_items'),
    path('detail/<int:pk>/', BookDetail.as_view(), name='book_detail_url'),
    path('cart/', views.cart_view, name='cart_url'),
    path('add-item-to-cart/<int:pk>', views.add_item_to_cart, name = 'add_item_to_cart'),
    path('abot/', about , name = 'about_url'),
    path('delete_item/<int:pk>', views.CartDeleteItem.as_view(), name='cart_delete_item'),
    path('delete_item_2/<int:pk>', cart_remove, name='cart_delete_item_2'),
    path('make-order/', views.make_order, name='make_order'),

]
