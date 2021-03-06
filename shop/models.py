from decimal import Decimal

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models, transaction

# Create your models here.
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.urls import reverse
from hitcount.models import HitCount, HitCountMixin

''' https://it4each.com/blog/dropshipping-internet-magazin-na-django-chast-5/'''

'''
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True, db_index=True)
    icon = models.FileField(blank=True) #upload_to="category/"
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

'''
class Writer(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True, db_index=True)
    bio = models.TextField()
    pic = models.FileField(blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('writer_url', kwargs={'slug': self.slug})


class Books(models.Model, HitCountMixin):
    title = models.CharField(max_length=150, db_index=True)
    code = models.CharField(max_length=255, verbose_name='product_code')
    writer = models.ForeignKey(Writer, on_delete=models.CASCADE)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='photos/%Y/', blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
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


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # on_delete=models.CASCADE ?????????????????????? User + ?????? ???? ?? ?????? ??????????????
    amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)

    # ?????????? ????????????????????, ?????????????? ???? ???????????? ???????????????? ?????????? ???????????? ???? ???????????????????? class Meta
    # https://django.fun/docs/django/ru/4.0/ref/models/options/
    # ?????????? ???????????????????????????? ?????? ?????????????? ????????????????????, ?????????????????????? ???????????????? # db_table
    class Meta:
        ordering = ['pk']  # ????????????????????
        # ???????????????????????? ?? ??????????????

    def __str__(self):
        return f'{self.user} --- {self.amount}'

    @staticmethod
    def get_balance(user: User):
        amount = Payment.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum']
        return amount or Decimal(0)


# ?????????????? ???????????? + CART
class Order(models.Model):
    STATUS_CART = '1_cart'
    STATUS_WAITING_FOR_PAYMENT = '2_waiting_for_payment'
    STATUS_PAID = '3_paid'
    STATUS_CHOICES = [
        (STATUS_CART, 'cart'),
        (STATUS_WAITING_FOR_PAYMENT, 'waiting_for_paymenr'),
        (STATUS_PAID, 'paid')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # items = models.ManyToManyField(OrderItem, related_name='orders')
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_CART)
    amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return f'{self.user} --- {self.amount} --- {self.status}'

    @staticmethod
    def get_cart(user: User):
        cart = Order.objects.filter(user=user,
                                    status=Order.STATUS_CART).first()
        if not cart:
            cart = Order.objects.create(user=user,
                                        status=Order.STATUS_CART, amount=0)
        return cart

    def get_amount(self):  # ???????? ????????
        amount = Decimal(0)
        for item in self.orderitem_set.all():
            amount += item.amount
        return amount

    def make_order(self):
        items = self.orderitem_set.all()
        if items and self.status == Order.STATUS_CART:
            self.status = Order.STATUS_WAITING_FOR_PAYMENT
            self.save()
            auto_payment_unpaid_orders(self.user)


'''
?????? ???????????? ?????????? ???????????????????? (????????????????, ??????????????????) ???????????????????? (?????? ????????) ????????????, ?????????? ?????????? ???????????? ???????????? ?????????????????????????? ??????????????????????????????'''


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Books, on_delete=models.PROTECT, db_index=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    discount = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    # objects = models.Manager() ???????? ?????????????? ???????? objects
    class Meta:
        ordering = ['pk']

    def __str__(self):
        return f'{self.quantity} --- {self.price} --- {self.discount}'

    @property
    def amount(self):
        return self.quantity * (self.price - self.discount)

    def get_absolute_url(self):
        return reverse('book_detail_url', kwargs={'pk':self.pk})

    def remove(self, book):
        book_id = str(book.id)
        if book_id in self.product:
            del self.product[book_id]
            self.save()

@transaction.atomic() # ???????????????? ?????? ?????? ?????????????? ?????? ????????????
def auto_payment_unpaid_orders(user: User):
    unpaid_orders = Order.objects.filter(user = user, status=Order.STATUS_WAITING_FOR_PAYMENT)
    for order in unpaid_orders:
        if Payment.get_balance(user) < order.amount:
            break
        order.payment = Payment.objects.all().last()
        order.status = Order.STATUS_PAID
        order.save()
        Payment.objects.create(user=user, amount=-order.amount)
@receiver(post_save, sender=OrderItem)
def recalculate_order_amount_after_save(sender, instance, **kwargs):
    order = instance.order
    order.amount = order.get_amount()
    order.save()


@receiver(post_delete, sender=OrderItem)
def recalculate_order_amount_after_delete(sender, instance, **kwargs):
    order = instance.order
    order.amount = order.get_amount()
    order.delete()

@receiver(post_delete, sender=Payment)
def auto_pay(sender, instance, **kwargs):
    user = instance.user
    auto_payment_unpaid_orders(user)
