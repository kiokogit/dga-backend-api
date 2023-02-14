# Generated by Django 4.1.3 on 2023-02-13 21:54

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('packages_service', '0012_alter_packagemodel_package_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packagemodel',
            name='package_id',
            field=models.UUIDField(default=uuid.UUID('bf7d06ae-7a5f-4684-9ba5-e16cfc26bd75'), editable=False),
        ),
    ]