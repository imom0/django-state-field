django-state-field 
==================

[![Build Status](https://api.travis-ci.org/imom0/django-state-field.png)](https://travis-ci.org/imom0/django-state-field)

django-state-field is a reusable Django app, providing a custom field called StateField for changing states. It is a simple state machine for your app to limit state changes.

Install
-------

Install django-state-field with pip:

    pip install django-state-field
    
or download tarball source file from github and extract it:

    python setup.py install
    
Configure
---------

Add `state_field` to your `settings.py`'s `INSTALLED_APPS`:

    INSTALLED_APPS = (
        ...
        'state_field',
        ...
    )

Use
---

Define your model:

    from django.db import models
    from state_field.fields import StateField
    
    flow = {
               'default_state': ['next_state', 'default_state'],
    	       'next_state': ['previous_state', 'default_state']
    	   }
    
    class Book(models.Model):
        state = StateField(max_length=20, state_flow=flow)

Change state in your app:

    >>> book = Book.objects.create(default='default_state')
    >>> book.state = 'next_state' # This is allowed
    >>> book.state = 'next_state' # Raises an exception
    >>> book.state = 'state_not_in_flow' # Raises an exception, too
