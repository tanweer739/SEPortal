from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import os

TYPE_CHOICES = [
    ('Sickday', 'SickDay'),
    ('Vacation', 'Vacation')
]


# Create your models here.
class Leave(models.Model):
    type = models.CharField(verbose_name="Leave Type", max_length=20, choices=TYPE_CHOICES)
    begindate = models.DateTimeField()
    enddate = models.DateTimeField()
    date_posted = models.DateTimeField(default=timezone.now)
    document = models.FileField(blank=True, default=None, upload_to='documents')
    title = models.TextField(max_length=100)
    content = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_accepted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('leave-home')

    @property
    def difference(self):
        return (self.enddate - self.begindate).days

    @property
    def totalleave(self):
        leaves = Leave.objects.all()
        total_leaves = 0
        for leave in leaves:
            total_leaves += leave.difference
        return total_leaves

    @property
    def filename(self):
        return os.path.basename(self.document.path)

    def accept(self):
        temp = Leave.objects.get(pk=self.pk)
        print(temp)
        temp.is_accepted = True
        temp.save()

    def reject(self):
        temp = Leave.objects.get(pk=self.pk)
        print(temp)
        temp.is_accepted = True
        temp.save()


class Reply(models.Model):
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    leave = models.ForeignKey(Leave, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('leave-detail', kwargs={'pk': self.leave_id})
