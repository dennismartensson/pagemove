# encoding: utf-8
from django import forms
from .models import URL


class URLForm(forms.ModelForm):

    class Meta:
        model = URL
        fields = ['url']
        widgets = {
            'url': forms.TextInput(attrs={'class': 'memberfield'})
        }
