# Generated by Django 4.2.1 on 2023-07-07 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_driver_per_km_alter_company_per_km'),
    ]

    operations = [
        migrations.AddField(
            model_name='company3ver',
            name='weekends',
            field=models.CharField(blank=True, choices=[('MON', 'MON'), ('TUE', 'TUE'), ('WEN', 'WEN'), ('TR', 'TR'), ('FRI', 'FRI'), ('SAT', 'SAT'), ('SUN', 'SUN')], default='', max_length=10),
        ),
    ]