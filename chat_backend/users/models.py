from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.models import User;
import uuid

class ConversationModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    conversation_title = models.CharField(max_length=255)  # 聊天名称
    created_at = models.DateTimeField(auto_now_add=True) # 创建时间

    def __str__(self):
        return self.conversation_title
    
class MessageModel(models.Model):
    conversation = models.ForeignKey(ConversationModel, on_delete=models.CASCADE)
    message_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # 消息ID
    message_role = models.CharField(max_length=10, choices=[('user', 'User'), ('ai', 'AI')])  # 消息发送者
    message_content = models.TextField()  # 消息内容
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message_id
    
class FileModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(ConversationModel, on_delete=models.CASCADE, default=1)
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
    
