# Generated by Django 3.1.3 on 2021-02-10 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kbl', '0007_auto_20210210_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='pushnotification',
            name='title',
            field=models.CharField(default='', max_length=50, verbose_name='Title'),
            preserve_default=False,
        ),
    ]
