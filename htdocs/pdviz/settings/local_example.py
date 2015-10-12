from base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'replace_with_your_db_name',  # Or path to database file if using sqlite3.
        'USER': 'replace_with_your_db_user',  # Not used with sqlite3.
        'PASSWORD': 'replace_with_your_db_password',  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {
            'sql_mode': 'traditional',
        },      
    }           
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'YOUR_SECRET_KEY_GOES_HERE...MAKE_SURE_TO_UPDATE_IT!!!'
                
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.example.org'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'no-reply@example.org'
EMAIL_HOST_PASSWORD = 'password'
DEFAULT_FROM_EMAIL = 'no-reply@example.org'
SERVER_EMAIL = "admin@example.org"
DEFAULT_TO_EMAIL = SERVER_EMAIL