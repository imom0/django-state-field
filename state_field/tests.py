from django.test import TestCase
from django.db import models

from state_field.fields import StateField, StateDescriptor
from state_field.exceptions import StateFieldError

flow = {
    'default_value': ['next', 'default_value', 'prev'],
    'next': ['next', 'default_value']
}


class Book(models.Model):

    state = StateField(max_length=20, state_flow=flow, default='default_value')

#TODO: better way to test signals sent or not

myflow = {'foo': ['bar']}

TEST_VALUE = 'foo'


class MyStateDescriptor(StateDescriptor):
    def state_foo_to_bar(self):
        global TEST_VALUE
        TEST_VALUE = 'bar'


class MyStateField(StateField):
    descriptor = MyStateDescriptor


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


class StateDescriptorTest(TestCase):

    def test_send_signal(self):

        book = MyBook.objects.create()
        self.assertEqual(TEST_VALUE, 'foo')
        book.state = 'bar'
        self.assertEqual(TEST_VALUE, 'bar')
