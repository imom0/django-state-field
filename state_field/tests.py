from mock import patch
from django.test import TestCase
from django.db import models

from state_field.fields import StateField
from state_field.exceptions import StateFieldError

flow = {
    'default_value': ['next', 'default_value', 'prev'],
    'next': ['next', 'default_value']
}


class Book(models.Model):

    state = StateField(max_length=20, state_flow=flow, default='default_value')

myflow = {'foo': ['bar']}


class MyStateField(StateField):

    def foo_to_bar(self):
        pass


class MyBook(models.Model):
    state = MyStateField(max_length=20, state_flow=myflow, default='foo')


class StateFieldTest(TestCase):

    def test_create_default_value(self):
        book = Book.objects.create()
        self.assertEqual(book.state, 'default_value')

    def test_create_not_default_value(self):
        book = Book.objects.create(state='next')
        self.assertEqual(book.state, 'next')

    def test_change_state_success(self):
        book = Book.objects.create()
        book2 = Book.objects.create(state='default_value')
        book.state = 'next'
        book.save()
        self.assertEqual(book.state, 'next')
        self.assertEqual(book2.state, 'default_value')

    def test_change_state_fail(self):
        book = Book.objects.create(state='next')

        def set_not_allowed_value():
            book.state = 'prev'

        self.assertRaises(StateFieldError, set_not_allowed_value)


@patch.object(MyStateField, 'foo_to_bar')
class StateDescriptorTest(TestCase):

    def test_hook(self, mock_method):
        book = MyBook.objects.create()
        self.assertFalse(mock_method.called)
        book.state = 'bar'
        self.assertTrue(mock_method.called)
