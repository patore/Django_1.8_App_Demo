from .base import *

DEBUG=False
ADMINS = [('user', 'user@domain.com')]
ALLOWED_HOSTS = ['.dummy_appapp.app.com']
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
