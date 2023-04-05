from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category


class Desk(models.Model):
    STATUS_TYPE = (
        ('accepted', 'accepted'),
        ('completed', 'completed'),
    )
    User = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    comment = models.TextField(max_length=2000)
    image = models.FileField(null=True, blank=True)
    status = models.CharField(
        choices=STATUS_TYPE,
        max_length=30,
        default='Accepted',
    )

    def __str__(self):
        return self.title


class DeskImage(models.Model):
    desk = models.ForeignKey(
        Desk,
        default=None,
        on_delete=models.CASCADE,
        related_name='img',
    )
    images = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return f'Image id: {self.pk}'

