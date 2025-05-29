from django import forms
from .models import Posts,CustomUser

class PostsForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['titulo', 'descriçao', 'img']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class PositionForm(forms.Form):
    position = forms.CharField()

from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

   