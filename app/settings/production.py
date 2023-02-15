from dotenv import load_dotenv
import os
from pathlib import Path

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-g$1n#9%#q1(_a_!m_#e&j=js)zf-=e5a8m+(fa#l=z*9ro*-s4'

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    'default':{
        'ENGINE':'django.db.backends.sqlite3',
         'NAME': BASE_DIR / 'db.sqlite3'
        
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('DATABASE_NAME'),
#         'USER': os.environ.get('DATABASE_USERNAME'),
#         'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
#         'CONN_MAX_AGE': 1000,
#         'OPTIONS': {
#             'options': '-c search_path={}'.format(os.environ.get('DATABASE_SCHEMA'))
#         },
#         'HOST': str(os.environ.get('DATABASE_HOST')),
#         'PORT': int(os.environ.get('DATABASE_PORT')), #type: ignore
#         'TEST': {
#             'ENGINE': 'django.db.backends.postgresql_psycopg2',
#             'NAME': os.environ.get('DATABASE_NAME'),
#             'USER': os.environ.get('DATABASE_USERNAME'),
#             'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
#             'OPTIONS': {
#                 'options': '-c search_path={}'.format(os.environ.get('DATABASE_SCHEMA'))
#             },

#         },
#     }
# }