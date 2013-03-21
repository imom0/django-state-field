import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from django.db.models.fields import CharField

from state_field.exceptions import StateFieldError


class StateDescriptor(object):
    _cache = None

    def __init__(self, field, flow):
        self.field = field
        self.flow = flow

    def __get__(self, instance, instance_type=None):
        if instance is None:
            raise AttributeError('State must be accessed via instance.')
        logger.debug('** call get **: %s' % (self._cache,))
        return self._cache

    def __set__(self, instance, value):
        current_value = self._cache
        logger.debug('** call set **: %s' % (current_value,))
        allowed_states = self.flow.get(current_value, [])
        if current_value is not None and value not in allowed_states:
            raise StateFieldError('Set state to %s is not allowed.' % value)
        self._cache = value
        self.send_signal(current_value, value)

    def send_signal(self, old_state, state):
        attrname = 'state_%s_to_%s' % (old_state, state)
        if hasattr(self, attrname):
            getattr(self, attrname)()


class StateField(CharField):
    """Custom field for storing state,
    Currently, StateField inherits from CharField, that means you can not
    set instance.state to 1 or other python objects if you define state a
    StateField, strings only now.You should pass state_flow argument to
    StateField, or an exception will be raised.
    """

    descriptor = StateDescriptor
    description = 'StateField'

    def __init__(self, *args, **kwargs):
        # FIXME: use validators
        if ('state_flow' not in kwargs or
                not isinstance(kwargs['state_flow'], dict)):
            raise StateFieldError('Must provide `state_flow` for StateField.')
        self.state_flow = kwargs.pop('state_flow')
        super(StateField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        super(StateField, self).contribute_to_class(cls, name)
        setattr(cls, self.name, self.descriptor(self, self.state_flow))
