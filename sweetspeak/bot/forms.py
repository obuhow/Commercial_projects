from django import forms

from .models import ScheduledPosts, PublishedPosts


class ScheduledPostsAdminForms(forms.ModelForm):

    class Meta:
        model = ScheduledPosts
        fields = ('sending_datetime', 'channel_id', 'url', 'post')
        widgets = dict(sending_datetime=forms.DateTimeInput,
                       url=forms.URLInput)

class PublishedPostsAdminForms(forms.ModelForm):

    class Meta:
        model = PublishedPosts
        fields = ('sending_datetime_p', 'channel_id_p', 'url_p', 'post_p')
        widgets = dict(sending_datetime_p=forms.DateTimeInput,
                       url_p=forms.URLInput)