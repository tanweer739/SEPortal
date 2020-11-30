from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import os


# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.FileField(blank=True, default=None, upload_to='documents')

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    @property
    def filename(self):
        return os.path.basename(self.document.path)


class Comment(models.Model):
    date_posted = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    document = models.FileField(blank=True, default=None, upload_to='documents')

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.post_id})

    @property
    def filename(self):
        return os.path.basename(self.document.path)
