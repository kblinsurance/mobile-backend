# Generated by Django 3.1.3 on 2021-03-10 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kbl', '0017_policy_in_active_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='policy',
            name='referrer',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Referrer'),
        ),
    ]