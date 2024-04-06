# models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}/{2}'.format(instance.user.id, instance.filename, filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    document = models.FileField(upload_to=user_directory_path, validators=[FileExtensionValidator(['pdf', 'jpg', 'png'])])
    filename = models.CharField(max_length=255)  # New field for filename
