# Generated by Django 4.1.3 on 2023-02-14 13:04

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('packages_service', '0018_alter_packagemodel_package_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packagemodel',
            name='package_id',
            field=models.UUIDField(default=uuid.UUID('858929a5-793a-46c2-a293-f10a60eb36f8'), editable=False),
        ),
    ]