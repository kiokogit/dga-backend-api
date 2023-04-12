from dotenv import load_dotenv
import os
from pathlib import Path

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-g$1n#9%#q1(_a_!m_#e&j=js)zf-=e5a8m+(fa#l=z*9ro*-s4'

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
        'default': {
            'ENGINE': 'djongo',
            'NAME': 'dga-staging',
            'ENFORCE_SCHEMA': False,
            'CLIENT': {
                'host':'mongodb+srv://dgatours:dgatours@dga-production.9lwhch8.mongodb.net/?retryWrites=true&w=majority',
                'port': 27017,
                'username': 'dgatours',
                'password': 'dgatours',
                'authSource': 'dga-staging',
                'authMechanism': 'SCRAM-SHA-1'
            },
            # 'LOGGING': {
            #     'version': 1,
            #     'loggers': {
            #         'djongo': {
            #             # 'level': 'INFO',
            #             # 'propagate': False,                        
            #         }
            #     },
            #  },
        }
    }

# DATABASES = {
#         'default': {
#             'ENGINE': 'djongo',
#             'NAME': os.environ.get('DBNAME'),
#             'ENFORCE_SCHEMA': False,
#             'CLIENT': {
#                 'host': os.environ.get('DBHOST'),
#                 'port': os.environ.get('DBPORT'),
#                 'username': os.environ.get('DBUSER'),
#                 'password': os.environ.get('DBPASS'),
#                 'authSource': os.environ.get('DBNAME'),
#                 'authMechanism': 'SCRAM-SHA-1'
#             },
#             # 'LOGGING': {
#             #     'version': 1,
#             #     'loggers': {
#             #         'djongo': {
#             #             # 'level': 'INFO',
#             #             # 'propagate': False,                        
#             #         }
#             #     },
#             #  },
#         }
#     }


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get('DBNAME'),
#         'USER': os.environ.get('DBUSER'),
#         'PASSWORD': os.environ.get('DBPASS'),
#         'CONN_MAX_AGE': 1000,
#         'OPTIONS': {
#             'options': '-c search_path={}'.format(os.environ.get('DBSCHEMA'))
#         },
#         'HOST': str(os.environ.get('DBHOST')),
#         'PORT': int(os.environ.get('DBPORT')), #type: ignore
#         'TEST': {
#             'ENGINE': 'django.db.backends.postgresql',
#             'NAME': os.environ.get('DBNAME'),
#             'USER': os.environ.get('DBUSER'),
#             'PASSWORD': os.environ.get('DBPASS'),
#             'OPTIONS': {
#                 'options': '-c search_path={}'.format(os.environ.get('DBSCHEMA'))
#             },

#         },
#     }
# }