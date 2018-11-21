from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Notify)
class NotifyAdmin(admin.ModelAdmin):
    list_display = (
        'creator',
        'to',
        'notify_type',
    )
