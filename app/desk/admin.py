from django.contrib import admin
from django.contrib.admin import ModelAdmin

from desk.models import Category, Desk, DeskImage


class DeskImageAdmin(admin.StackedInline):
    model = DeskImage


@admin.register(Desk)
class DeskAdminPanel(ModelAdmin):
    inlines = [DeskImageAdmin]

    class Meta:
        model = Desk


@admin.register(Category)
class CategoryAdminPanel(ModelAdmin):
    pass


@admin.register(DeskImage)
class ImageAdminPanel(ModelAdmin):
    pass
