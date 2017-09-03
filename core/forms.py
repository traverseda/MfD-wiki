from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from core.models import Wiki

User = get_user_model()

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email','password1', 'password2', )

class WikiForm(ModelForm):
     commit_message = forms.CharField(max_length=300, required=False)
     class Meta:
         model = Wiki
         fields = ['name','bodyText','tags']
