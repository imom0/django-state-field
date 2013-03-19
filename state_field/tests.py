from django.test import TestCase
from django.db import models

from state_field.fields import StateField

flow = {
    'default_value': ['next', 'default_value', 'prev'],
    'next': ['next', 'default_value']
}


class Book(models.Model):

    state = StateField(max_length=20, state_flow=flow, default='default_value')


class StateFieldTest(TestCase):

    def test_create_default_value(self):
        book = Book.objects.create()
        self.assertEqual(book.state, 'default_value')

    def test_create_not_default_value(self):
        book = Book.objects.create(state='next')
        self.assertEqual(book.state, 'next')
