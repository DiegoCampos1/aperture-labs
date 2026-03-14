from django.contrib import admin

from .models import Clock, Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name")
    search_fields = ("first_name", "last_name")


@admin.register(Clock)
class ClockAdmin(admin.ModelAdmin):
    list_display = ("employee", "clock_in_datetime", "clock_out_datetime")
    list_filter = ("employee",)
