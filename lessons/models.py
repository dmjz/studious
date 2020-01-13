import uuid
from django.db import models
from django.contrib.auth.models import User
from core.models import Profile

class Lesson(models.Model):
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField()
