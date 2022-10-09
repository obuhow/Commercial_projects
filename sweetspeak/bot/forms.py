from django import forms

from .models import Bot


class BotAdminForms(forms.ModelForm):

    class Meta:
        model = Bot
        fields = ('sending_datetime', 'channel_id', 'url', 'post')
        widgets = dict(sending_datetime=forms.DateTimeInput,
                       url=forms.URLInput)