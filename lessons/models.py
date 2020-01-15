import uuid
import os
from django.db import models
from django.contrib.auth.models import User
from core.models import Profile
from django.core.files.storage import FileSystemStorage

storage = FileSystemStorage()

def user_directory_path(instance, filename):
    """ Return lesson upload filepath: MEDIA_ROOT/owner_uuid/lesson_uuid """

    return os.path.join(str(instance.owner.profile.uuid), str(instance.uuid))

class Lesson(models.Model):
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.TextField(default='Untitled', max_length=500)
    created = models.DateTimeField()
    file = models.FileField(upload_to=user_directory_path, storage=storage, max_length=200)

    def __str__(self):
        return f'<Lesson { self.id }: { self.owner } { self.created }>'
