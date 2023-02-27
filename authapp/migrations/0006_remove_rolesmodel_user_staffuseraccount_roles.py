# Generated by Django 4.1.3 on 2023-02-15 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0005_alter_departmentmodel_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rolesmodel',
            name='user',
        ),
        migrations.AddField(
            model_name='staffuseraccount',
            name='roles',
            field=models.ManyToManyField(related_name='user_roles', to='authapp.rolesmodel'),
        ),
    ]
