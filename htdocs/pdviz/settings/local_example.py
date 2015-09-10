from base import *
import django.conf.global_settings as DEFAULT_SETTINGS
from django.contrib.messages import constants as message

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'YOUR_SECRET_KEY_GOES_HERE...MAKE_SURE_TO_UPDATE_IT!!!'


CRISPY_TEMPLATE_PACK='bootstrap3'


### This is to map Django message levels to Boostrap3 alert levels ########
MESSAGE_TAGS = {message.DEBUG: 'debug',
                message.INFO: 'info',
                message.SUCCESS: 'success',
                message.WARNING: 'warning',
                message.ERROR: 'danger',}
                
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.example.org'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'no-reply@example.org'
EMAIL_HOST_PASSWORD = 'password'
DEFAULT_FROM_EMAIL = 'no-reply@example.org'
SERVER_EMAIL = "admin@example.org"
DEFAULT_TO_EMAIL = SERVER_EMAIL