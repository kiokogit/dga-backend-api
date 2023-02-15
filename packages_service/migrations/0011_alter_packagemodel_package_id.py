# Generated by Django 4.1.3 on 2023-02-13 21:53

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('packages_service', '0010_alter_packagemodel_package_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packagemodel',
            name='package_id',
            field=models.UUIDField(default=uuid.UUID('4f594f3a-981b-40f9-a1ec-4d1e0aded481'), editable=False),
        ),
    ]
