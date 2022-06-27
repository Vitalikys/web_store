from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ('id', 'writer', 'title','code', 'price','photo' ,'get_photo','is_availible')
    # list_display = '__all__'
    fields = ('title','writer', 'code', 'description', 'price','photo' ,'get_photo','is_availible')
    list_editable = ('is_availible', 'price')
    list_display_links = ('id', 'title')
    search_fields = ('title','description',)
    readonly_fields = ('get_photo',)

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src ="{obj.photo.url}" width="35">')

    save_on_top = True
'''
You can’t use this @decorator if you have to reference your model admin class in 
its __init__() method, e.g. super(PersonAdmin, self).__init__(*args, **kwargs). 
 You can use super().__init__(*args, **kwargs).'''


# admin.site.register(Books, BooksAdmin)
admin.site.register(Writer)
admin.site.register(Payment)
admin.site.register(OrderItem)
admin.site.register(Order)
# Register your models here.
admin.site.site_title = 'Керування сайтом'
admin.site.site_header = 'Керування магазином'