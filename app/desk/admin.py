from django.contrib import admin
from django.contrib.admin import ModelAdmin

from desk.models import Category, Desk


@admin.register(Category)
@admin.register(Desk)
class AdminPanel(ModelAdmin):
    pass
