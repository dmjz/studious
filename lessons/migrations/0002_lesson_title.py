# Generated by Django 3.0.1 on 2020-01-15 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='title',
            field=models.TextField(default='Untitled', max_length=500),
        ),
    ]
