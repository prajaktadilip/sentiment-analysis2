# Generated by Django 2.2.7 on 2020-01-16 10:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sentiment', '0005_auto_20200116_1519'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='overall_rating1',
            name='user',
        ),
    ]
