# Generated by Django 4.2.1 on 2023-07-07 04:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_company3ver_weekends'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company3ver',
            name='weekends',
        ),
    ]
