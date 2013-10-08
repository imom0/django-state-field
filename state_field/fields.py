import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from django.conf import settings
from django.db.models.fields import CharField

from state_field.exceptions import StateFieldError

HOOK_FORMAT = getattr(settings, 'STATE_FIELD_HOOK_FORMAT', 'state_%s_to_%s')


class StateDescriptor(object):

    def __init__(self, field):
        self.field = field
        self.flow = field.state_flow

    def __get__(self, instance, instance_type=None):
        if instance is None:
            raise AttributeError('State must be accessed via instance.')
        current_state = instance.__dict__.get(self.field.name, None)
        logger.debug('** call get **: %s' % (current_state,))
        return current_state

    def __set__(self, instance, state):
        current_state = self.__get__(instance, instance.__class__)
        logger.debug('** call set **: %s' % (current_state,))
        allowed_states = self.flow.get(current_state, [])
        if current_state is not None and state not in allowed_states:
            raise StateFieldError('Set state to %s is not allowed.' % state)
        instance.__dict__[self.field.name] = state
        self.call_hook(current_state, state)

    def call_hook(self, older_state, state):
        attrname = HOOK_FORMAT % (older_state, state)
        if hasattr(self.field, attrname):
            try:
                getattr(self.field, attrname)()
            except:
                logger.error('Error in hooks.', exc_info=True)


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
        setattr(cls, self.name, self.descriptor(self))
