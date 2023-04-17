from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-g$1n#9%#q1(_a_!m_#e&j=js)zf-=e5a8m+(fa#l=z*9ro*-s4'

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'd8bipld7hv4jjo',
#         'USER': 'pqcwpbjatjxdjf',
#         'PASSWORD': 'e4888706932d04a041656a840fab7671169720c234565ed269658aed01c178d8',
#         'OPTIONS': {
#             'options': '-c search_path=public'
#         },
#         'HOST': 'ec2-3-229-161-70.compute-1.amazonaws.com',
#         'PORT': 5432
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DBNAME'),
        'USER': os.environ.get('DBUSER'),
        'PASSWORD': os.environ.get('DBPASS'),
        'CONN_MAX_AGE': 1000,
        'OPTIONS': {
            'options': '-c search_path={}'.format(os.environ.get('DBSCHEMA'))
        },
        'HOST': os.environ.get('DBHOST'),
        'PORT': int(os.environ.get('DBPORT')), #type: ignore
        'TEST': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('DBNAME'),
            'USER': os.environ.get('DBUSER'),
            'PASSWORD': os.environ.get('DBPASS'),
            'OPTIONS': {
                'options': '-c search_path={}'.format(os.environ.get('DBSCHEMA'))
            },

        },
    }
}