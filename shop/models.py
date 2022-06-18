from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

# Create your models here.
from django.urls import reverse
from hitcount.models import HitCount, HitCountMixin


# class Category(models.Model):
#     name = models.CharField(max_length=100)
#     slug = models.SlugField(max_length=150, unique=True, db_index=True)
#     icon = models.FileField(blank=True) #upload_to="category/"
#     create_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateField(auto_now=True)
#
#     def __str__(self):
#         return self.name


# class Writer(models.Model):
#     name = models.CharField(max_length=100)
#     slug = models.SlugField(max_length=150, unique=True, db_index=True)
#     bio = models.TextField()
#     pic = models.FileField(blank=True)
#     create_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateField(auto_now=True)
#
#     def __str__(self):
#         return self.name


class Books(models.Model, HitCountMixin):
    title = models.CharField(max_length=150)
    # writer = models.ForeignKey(Writer, on_delete=models.CASCADE)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    photo = models.ImageField(blank=True)
    price = models.IntegerField(default=0)
    # created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateField(auto_now=True)
    is_availible = models.BooleanField(default=True)
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')

    def get_absolute_url(self):
        return reverse('book_detail_url', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title
