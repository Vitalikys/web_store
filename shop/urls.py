from django.urls import path, include

from .views import *

urlpatterns = [
    path('', HomeLists.as_view(), name = 'list_items'),
    path('detail/<int:pk>/' , BookDetail.as_view(), name= 'book_detail_url'),

]