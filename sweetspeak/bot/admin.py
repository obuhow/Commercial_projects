from django.contrib import admin

from .models import ScheduledPosts, PublishedPosts
from .forms import ScheduledPostsAdminForms

@admin.register(ScheduledPosts)
class ScheduledPostsAdmin(admin.ModelAdmin):
    list_display = ('sending_datetime', 'channel_id', 'url', 'post')
    form = ScheduledPostsAdminForms

@admin.register(PublishedPosts)
class PublishedPostsAdmin(ScheduledPostsAdmin):
    pass
