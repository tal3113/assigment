from django.contrib import admin

from .models import Message


class MessageAdmin(admin.ModelAdmin):
    exclude = ('read',)


admin.site.register(Message, MessageAdmin)
