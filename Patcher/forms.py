# -*- coding: utf-8 -*-
from django import forms

from Patcher.models import File

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        exclude = ('filename','version', 'action','created')
