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
	first_name = forms.CharField(max_length=30, required=True)
	last_name = forms.CharField(max_length=30, required=True)
	username = forms.EmailField(max_length=254, required=True)
	password1 = forms.CharField(
		widget=forms.PasswordInput(attrs={'class':'password'}))
	password2 = forms.CharField(
		widget=forms.PasswordInput(attrs={'class':'password'}))

	#reCAPTCHA token
	token = forms.CharField(
		widget=forms.HiddenInput())

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'password1', 'password2', )


class AuthForm(AuthenticationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]