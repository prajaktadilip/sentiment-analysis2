# Generated by Django 3.0.1 on 2020-01-17 05:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Process', '0008_auto_20200116_1828'),
    ]

    operations = [
        migrations.CreateModel(
            name='Filedata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=100)),
                ('filetype', models.FileField(upload_to='filefolder')),
                ('process_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('positive', models.FloatField()),
                ('negative', models.FloatField()),
                ('neutral', models.FloatField()),
            ],
        ),
        migrations.DeleteModel(
            name='overall_rating1',
        ),
    ]
