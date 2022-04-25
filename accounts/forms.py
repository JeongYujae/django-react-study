from django.contrib.auth.forms import AuthenticationForm
from attr import field, fields
from django import forms
from .models import Profile

# 프로필 수정하는 모델 구현
class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['address', 'zipcode']

class LoginForm(AuthenticationForm):
    answer=forms.IntegerField(help_text='3+3=?')

    def clean_answer(self):
        answer=self.cleaned_data.get('answer')
        if answer!=6:
            raise forms.ValidationError('오답!')
        return answer