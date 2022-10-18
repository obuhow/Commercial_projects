from django import forms

from .models import ScheduledPosts


class ScheduledPostsAdminForms(forms.ModelForm):

    class Meta:
        model = ScheduledPosts
        fields = ('sending_datetime', 'channel_id', 'url', 'post')
        widgets = dict(sending_datetime=forms.DateTimeInput,
                       url=forms.URLInput)