from django.forms import ModelForm, widgets
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from registration.models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'address',
            'town',
            'county',
            'postal_code',
            'country',
            'longitude',
            'latitude'
        ]


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
        ]


class AuthForm(AuthenticationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]