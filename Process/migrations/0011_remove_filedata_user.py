# Generated by Django 3.0.1 on 2020-01-17 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Process', '0010_filedata_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filedata',
            name='user',
        ),
    ]