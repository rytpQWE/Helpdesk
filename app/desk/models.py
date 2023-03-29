from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    category = models.CharField(max_length=100)


class Desk(models.Model):
    STATUS_TYPE = (
        ('accepted', 'Accepted'),
        ('in_progress', 'In progress'),
        ('completed', 'Completed'),
    )
    User = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    comment = models.TextField(max_length=2000)
    status = models.CharField(choices=STATUS_TYPE, max_length=30, default='Accepted')

