from django.contrib import admin
from .models import *
from django.apps import apps
# Register your models here.

apps_models = apps.get_models()

for model in apps_models:  
    try:
        admin.site.register(
            model
        )
    except admin.sites.AlreadyRegistered:
        pass
