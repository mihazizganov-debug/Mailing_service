from django.contrib import admin

from .models import Attempt, Client, Mailing, Message


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name")
    search_fields = ("email", "full_name")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject",)
    search_fields = ("subject",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("id", "start_time", "end_time", "status", "message")
    list_filter = ("status",)
    filter_horizontal = ("recipients",)


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ("attempt_time", "status", "mailing")
    list_filter = ("status",)
