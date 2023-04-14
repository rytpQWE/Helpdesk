from django.contrib import admin
from django.contrib.admin import ModelAdmin

from desk.models import Category, Desk, DeskImage, Employee


class DeskImageAdmin(admin.StackedInline):
    model = DeskImage


@admin.register(Desk)
class DeskAdminPanel(ModelAdmin):
    inlines = [DeskImageAdmin]
    readonly_fields = ('employee_comment', )

    class Meta:
        model = Desk


@admin.register(Category)
class CategoryAdminPanel(ModelAdmin):
    pass


@admin.register(DeskImage)
class ImageAdminPanel(ModelAdmin):
    pass


@admin.register(Employee)
class EmployeeAdminPanel(ModelAdmin):
    pass
