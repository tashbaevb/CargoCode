# Generated by Django 4.2.3 on 2023-07-05 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_driver_driver_license_alter_driver_straxovka'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='driver_license',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='driver',
            name='straxovka',
            field=models.TextField(blank=True, default=''),
        ),
    ]
