# Generated by Django 4.1.3 on 2023-02-09 07:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('packages_service', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packagemodel',
            name='package_id',
            field=models.UUIDField(default=uuid.UUID('a365ee22-1167-49f5-b2b3-40f7d7401b26'), editable=False),
        ),
    ]