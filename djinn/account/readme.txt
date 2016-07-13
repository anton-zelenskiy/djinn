add in settings.py:

AUTH_USER_MODEL = 'account.ExtUser'
AUTHENTICATION_BACKENDS = ['account.backends.EmailAuthBackend', 'django.contrib.auth.backends.ModelBackend']