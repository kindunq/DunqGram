from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.Notifications)
class NotificationsAdmin(admin.ModelAdmin):

    list_display = (
        'creator',
        'to',
        'notification_type',
    )
