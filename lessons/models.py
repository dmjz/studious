import uuid
import os
from django.db import models
from django.contrib.auth.models import User
from core.models import Profile
from studious.storage_backends import LessonStorage

def user_directory_path(instance, filename):
    """ Return lesson upload filepath: <media folder>/owner_uuid/lesson_uuid """

    return os.path.join(str(instance.owner.profile.uuid), str(instance.uuid))

class Lesson(models.Model):
    
    # UUID for storage on AWS
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    
    # "Metadata" fields
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.TextField(default='Untitled', max_length=500)
    created = models.DateTimeField()

    # File storage of lesson content
    file = models.FileField(upload_to=user_directory_path, storage=LessonStorage(), max_length=200)

    # Review fields
    review_stage = models.PositiveSmallIntegerField(default=0)
    next_review_time = models.DateTimeField(default=None, null=True)
    review_correct = models.PositiveIntegerField(default=0)
    review_incorrect = models.PositiveIntegerField(default=0)
    review_started = models.DateTimeField(default=None, null=True)

    def __str__(self):
        return f'<Lesson { self.id }: { self.owner }, { self.created }>'
