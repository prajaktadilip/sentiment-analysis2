# Generated by Django 2.2.7 on 2020-01-16 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sentiment', '0006_remove_overall_rating1_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='overall_rating1',
            name='filename',
            field=models.CharField(max_length=100),
        ),
    ]
