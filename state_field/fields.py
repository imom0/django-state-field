from django.db.models.fields import CharField

from state_field.exceptions import StateFieldError


class StateDescriptor(object):

    def __init__(self, field):
        self.field = field

    def __get__(self, instance, instance_type=None):
        if instance is None:
            raise AttributeError('State must be accessed via instance.')
        return instance.__dict__[self.field.name]

    def __set__(self, instance, value):
        if value != 'value_for_test':
            raise StateFieldError('Set state to %s is not allowed.' % value)
        instance.__dict__[self.field.name] = value


class StateField(CharField):

    description = 'StateField'

    def __init__(self, *args, **kwargs):
        # FIXME: use validators
        if ('state_flow' not in kwargs or
                not isinstance(kwargs['state_flow'], dict)):
            raise StateFieldError('Must provide `state_flow` for StateField.')
        super(StateField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        super(StateField, self).contribute_to_class(cls, name)
        setattr(cls, self.name, StateDescriptor(self))
