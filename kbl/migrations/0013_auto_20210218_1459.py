# Generated by Django 3.1.3 on 2021-02-18 13:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kbl', '0012_auto_20210218_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='start',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='Start Date'),
        ),
    ]
