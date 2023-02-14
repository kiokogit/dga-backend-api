# Generated by Django 4.1.3 on 2023-02-13 21:37

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('packages_service', '0006_alter_packagemodel_package_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packagemodel',
            name='package_id',
            field=models.UUIDField(default=uuid.UUID('f5ced2e5-1732-49be-94bb-660a1e72688f'), editable=False),
        ),
    ]