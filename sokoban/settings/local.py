from .base import *


DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sokoban',
        'USER': 'sokoban',
        'PASSWORD': 'sokoban',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    },
}