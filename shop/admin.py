from django.contrib import admin
from .models import *

class BooksAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'price','photo' ,'is_availible')
    # list_display = '__all__'
    fields = ('title', 'description', 'price','photo' ,'is_availible')
    list_editable = ('is_availible',)
    list_display_links = ('id', 'title')
    search_fields = ('title','description',)



admin.site.register(Books, BooksAdmin)
# Register your models here.
admin.site.site_title = 'Керування сайтом'
admin.site.site_header = 'Керування магазином'