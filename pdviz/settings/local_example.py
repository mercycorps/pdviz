import yaml
from .base import *
from os.path import dirname, join, abspath


SETTINGS_DIR = dirname(abspath(__file__))

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
SECRET_KEY = 'YOUR_SECRET_KEY_GOES_HERE...MAKE_SURE_TO_UPDATE_IT!!!'

DATABASES = {
    'default': {
        'NAME': 'pdviz',
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': '',
        'PORT': '',
    },
    'gait': {
        'NAME': 'grants',
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': '',
        'OPTIONS': {
            'charset': 'latin1',
        },
    }
}

DATABASE_ROUTERS = ['dataviz.models.DBRouter']

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.example.org'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'no-reply@example.org'
EMAIL_HOST_PASSWORD = 'password'
DEFAULT_FROM_EMAIL = 'no-reply@example.org'
SERVER_EMAIL = "admin@example.org"
DEFAULT_TO_EMAIL = SERVER_EMAIL

ADMINS = (
    ('Admins', 'admins@example.com'),
)
MANAGERS = ADMINS

"""
CRISPY_TEMPLATE_PACK='bootstrap3'


### This is to map Django message levels to Boostrap3 alert levels ########
MESSAGE_TAGS = {message.DEBUG: 'debug',
                message.INFO: 'info',
                message.SUCCESS: 'success',
                message.WARNING: 'warning',
                message.ERROR: 'danger',}
"""


# Social auth setup
def read_yaml(path):
    with open(path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data


saml_settings = read_yaml(join(SETTINGS_DIR, 'saml_config.yml'))

SOCIAL_AUTH_SAML_SP_ENTITY_ID = saml_settings.get('SOCIAL_AUTH_SAML_SP_ENTITY_ID', None)
SOCIAL_AUTH_SAML_SP_PUBLIC_CERT = saml_settings.get('SOCIAL_AUTH_SAML_SP_PUBLIC_CERT', None)
SOCIAL_AUTH_SAML_SP_PRIVATE_KEY = saml_settings.get('SOCIAL_AUTH_SAML_SP_PRIVATE_KEY', None)
SOCIAL_AUTH_SAML_ORG_INFO = saml_settings.get('SOCIAL_AUTH_SAML_ORG_INFO', None)
SOCIAL_AUTH_SAML_TECHNICAL_CONTACT = saml_settings.get('SOCIAL_AUTH_SAML_TECHNICAL_CONTACT', None)
SOCIAL_AUTH_SAML_SUPPORT_CONTACT = saml_settings.get('SOCIAL_AUTH_SAML_SUPPORT_CONTACT', None)
SOCIAL_AUTH_SAML_ENABLED_IDPS = saml_settings.get('SOCIAL_AUTH_SAML_ENABLED_IDPS', None)
