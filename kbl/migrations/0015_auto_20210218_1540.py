# Generated by Django 3.1.3 on 2021-02-18 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kbl', '0014_auto_20210218_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='percentage',
            field=models.CharField(choices=[('Quarterly', '25'), ('Half', '50'), ('Yearly', '100')], default='Yearly', max_length=50, verbose_name='Percentage'),
        ),
        migrations.AlterField(
            model_name='policy',
            name='duration',
            field=models.CharField(choices=[('Half Yearly', 'Half Yearly'), ('Quarterly', 'Quarterly'), ('Yearly', 'Yearly')], default='Yearly', max_length=50, verbose_name='Duration'),
        ),
    ]
