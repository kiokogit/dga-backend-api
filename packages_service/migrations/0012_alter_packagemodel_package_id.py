# Generated by Django 4.1.3 on 2023-02-13 21:54

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('packages_service', '0011_alter_packagemodel_package_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packagemodel',
            name='package_id',
            field=models.UUIDField(default=uuid.UUID('feb8d722-91c2-4657-866c-aac5c91b79ef'), editable=False),
        ),
    ]
