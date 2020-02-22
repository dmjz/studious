# Generated by Django 3.0.1 on 2020-02-21 12:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lessons', '0006_auto_20200216_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='original_lesson',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='lessons.Lesson'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='original_owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='original_owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lesson',
            name='times_copied',
            field=models.PositiveIntegerField(default=0),
        ),
    ]