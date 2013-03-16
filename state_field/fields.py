#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.db.models.fields import CharField


class StateDescriptor(object):

    def __init__(self, field):
        self.field = field

    def __get__(self, instance, instance_type=None):
        if instance is None:
            raise AttributeError('State must be accessed via instance')
        return instance.__dict__[self.field.name]

    def __set__(self, instance, value):
        instance.__dict__[self.field.name] = value


class StateField(CharField):

    description = u'StateField'
