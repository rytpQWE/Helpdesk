from django.contrib import admin

from desk.models import Category, Desk


@admin.register(Category)
@admin.register(Desk)
class AdminPanel:
    pass
