from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.test import TestCase
from shop.models import *


class TestDatabase(TestCase):
    fixtures = ['shop/fixtures/db.json']

    # def setUp(self):
    #     self.user = User.objects.get(username='admin')

    # @classmethod
    #     def setUpClass(cls):
    #         super().setUpClass()

    def test_user_exists(self):
        '''  assertEqual(first, second, msg=None)
             Test that first and second are equal. If the values do not compare equal, the test will fail.'''
        users = User.objects.all()
        users_number = users.count()
        user = users.first()
        self.assertEqual(users_number, 1)
        self.assertEqual(user.username, 'admin')
        self.assertTrue(user.is_superuser)

    def test_user_check_password(self):
        self.assertTrue(self.user.check_password('admin'))

    # перевірка чи є дані > 0
    def test_all_data(self):
        self.assertGreater(Books.objects.all().count(), 0)
        self.assertGreater(Order.objects.all().count(), 0)
        self.assertGreater(OrderItem.objects.all().count(), 0)
        self.assertGreater(Payment.objects.all().count(), 0)

    def find_cart_number(self):
        cart_number = Order.objects.filter(user=self.user,
                                           status=Order.STATUS_CART).count()
        return cart_number

# command to RUN:
# python manage.py tests shop.tests --failfast
# Create your tests here.
