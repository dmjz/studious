# Generated by Django 3.0.1 on 2020-01-13 13:25

from django.conf import settings
import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion
import lessons.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created', models.DateTimeField()),
                ('file', models.FileField(max_length=200, storage=django.core.files.storage.FileSystemStorage(), upload_to=lessons.models.user_directory_path)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
