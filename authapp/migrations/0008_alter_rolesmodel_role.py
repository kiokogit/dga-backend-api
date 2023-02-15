# Generated by Django 4.1.3 on 2023-02-15 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0007_remove_publicuseraccount_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rolesmodel',
            name='role',
            field=models.CharField(blank=True, choices=[('BOOKING MANAGER', 'BOOKING MANAGER'), ('FINANCE OFFICER', 'FINANCE OFFICER'), ('CUSTOMER CARE', 'CUSTOMER CARE'), ('ICT OFFICER', 'ICT OFFICER'), ('BOOKING OFFICER', 'BOOKING OFFICER'), ('GENERAL MANAGER', 'GENERAL MANAGER'), ('DIRECTOR', 'DIRECTOR'), ('GENERAL STAFF', 'GENERAL STAFF'), ('CEO', 'CEO')], max_length=25, null=True, unique=True),
        ),
    ]
