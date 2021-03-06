# Generated by Django 2.2.7 on 2020-01-17 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sentiment', '0014_auto_20200118_0118'),
    ]

    operations = [
        migrations.CreateModel(
            name='individual',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_text', models.TextField()),
                ('process_review', models.TextField()),
                ('positive', models.FloatField()),
                ('negative', models.FloatField()),
                ('neutral', models.FloatField()),
                ('rat', models.CharField(max_length=100)),
            ],
        ),
    ]
