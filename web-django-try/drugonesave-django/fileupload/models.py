from django.db import models

class FileUpload(models.Model):
    title = models.TextField(max_length=40, null=True)
    imgfile = models.ImageField(null=True, upload_to="", blank=True)
    content = models.TextField()

    def __str__(self):
        return self.title
# Create your models here.

class CameraImage(models.Model):
    image = models.ImageField(upload_to="media")
    timestamp = models.DateTimeField(auto_now_add=True)