# Generated by Django 4.2.1 on 2023-07-07 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_company3ver_weekends'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='weekends',
            field=models.CharField(blank=True, choices=[('MON', 'MON'), ('TUE', 'TUE'), ('WEN', 'WEN'), ('TR', 'TR'), ('FRI', 'FRI'), ('SAT', 'SAT'), ('SUN', 'SUN')], default='', help_text='Select weekends', max_length=10),
        ),
        migrations.AlterField(
            model_name='company3ver',
            name='weekends',
            field=models.CharField(blank=True, choices=[('MON', 'MON'), ('TUE', 'TUE'), ('WEN', 'WEN'), ('TR', 'TR'), ('FRI', 'FRI'), ('SAT', 'SAT'), ('SUN', 'SUN')], default='', help_text='Select weekends', max_length=10),
        ),
    ]
