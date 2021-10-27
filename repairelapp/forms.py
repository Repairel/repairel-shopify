from django import forms
from django.forms.widgets import HiddenInput


# Form fields will be revised later. Currently setting things up.
class ShoeRequestForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'col-md-6 form-it',
        'placeholder': 'Enter title for shoe'
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'col-md-12 form-it',
        'placeholder': 'Enter description for shoe'
    }))
    author = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'col-md-6 form-it',
        'placeholder': 'Your Name'
    }))


class LoginForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        # 'class': 'col-md-6 form-it',
        'placeholder': 'Your Name'
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        # 'class': 'col-md-6 form-it',
        'placeholder': 'yourname@example.com'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        # 'class': 'col-md-6 form-it',
        'placeholder': 'Your Password'
    }))
    image = forms.ImageField(required=False)


class RegistrationForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        # 'class': 'col-md-6 form-it',
        'placeholder': 'Your Name'
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        # 'class': 'col-md-6 form-it',
        'placeholder': 'yourname@example.com'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        # 'class': 'col-md-6 form-it',
        'placeholder': 'Your Password'
    }))
    image = forms.ImageField(required=False)