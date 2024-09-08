from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.models import User;

class FileModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='user_files/')
    filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()
    file_format = models.CharField(max_length=50)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Set file details before saving
        if self.file:
            self.filename = self.file.name
            self.file_size = self.file.size
            self.file_format = self.file.name.split('.')[-1]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.filename