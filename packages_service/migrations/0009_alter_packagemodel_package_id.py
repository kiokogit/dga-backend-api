# Generated by Django 4.1.3 on 2023-02-13 21:40

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('packages_service', '0008_alter_packagemodel_package_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packagemodel',
            name='package_id',
            field=models.UUIDField(default=uuid.UUID('69645a05-aed2-44ed-b707-225e5168a0da'), editable=False),
        ),
    ]
