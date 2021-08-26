# Generated by Django 3.1.3 on 2021-02-08 23:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('kbl', '0002_auto_20210208_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Issued Date'),
            preserve_default=False,
        ),
    ]
