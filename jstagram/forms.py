from email import message
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta: 
        model= Post
        fields=['message','photo','is_public']


    def clean_message(self):
        message=self.cleaned_data.get('message')
        return message