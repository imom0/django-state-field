from django.core.exceptions import FieldError


class StateFieldError(FieldError):
    '''State changes not allowed'''
    pass
