# Generated by Django 3.0.1 on 2020-01-16 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Process', '0002_filedata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filedata',
            name='negative',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='filedata',
            name='neutral',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='filedata',
            name='positive',
            field=models.FloatField(blank=True),
        ),
    ]
