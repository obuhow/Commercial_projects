from django.contrib import admin

from .models import Bot, PublishedPosts
from .forms import BotAdminForms

@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ('sending_datetime', 'channel_id', 'url', 'post')
    form = BotAdminForms

@admin.register(PublishedPosts)
class PublishedPostsAdmin(BotAdmin):
    pass
