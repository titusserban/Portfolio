from urllib import request
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.conf import settings
from django.http import JsonResponse
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import CreateView

from ProjectCoreDjango.mixins import AjaxFormMixin, recaptcha_validation, form_errors

from .forms import UserForm, UserProfileForm, AuthForm

# Default messages and results for form errors
result = "Error"
message = "There was an error, please try again"


# Basic template view for user account
class AccountView(LoginRequiredMixin, TemplateView):
	template_name = "registration/account.html"

def is_ajax(self):
    return self.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

# Function view to allow users to update their profile
def profile_view(request):
	user = request.user
	user_profile = user.userprofile

	form = UserProfileForm(instance = user_profile) 

	if is_ajax(request=request):
		form = UserProfileForm(data = request.POST, instance = user_profile)
		if form.is_valid():
			obj = form.save()
			obj.has_profile = True
			obj.save()
			result = "Success"
			message = "Your profile has been updated"
		else:
			message = form_errors(form)
		data = {'result': result, 'message': message}
		return JsonResponse(data)

	else:
		context = {'form': form}
		context['google_api_key'] = settings.GOOGLE_API_KEY
		context['base_country'] = settings.BASE_COUNTRY

		return render(request, 'registration/profile.html', context)


# Generic FormView for user sign-up with reCAPTCHA security
class SignUpView(FormView):

	template_name = "registration/sign_up.html"
	form_class = UserForm

	# reCAPTURE key required in context
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["recaptcha_site_key"] = settings.RECAPTCHA_PUBLIC_KEY
		return context

	def form_valid(self, form):
		response = super(SignUpView, self).form_valid(form)	

		token = form.cleaned_data.get('token')
		captcha = recaptcha_validation(token)
		if captcha["success"]:
			obj = form.save()
			obj.email = obj.username
			obj.save()
			user_profile = obj.userprofile
			user_profile.captcha_score = float(captcha["score"])
			user_profile.save()
			
			login(self.request, obj, backend='django.contrib.auth.backends.ModelBackend')

			#change result & message on success
			result = "Success"
			message = "Thank you for signing up"

		data = {'result': result, 'message': message}
		return JsonResponse(data)

	def form_invalid(self,form):
		return super().form_invalid(form)

	def get_success_url(self):
		return reverse('registration:sign-in')


# Generic FormView with AjaxFormMixin for user sign-in
class SignInView(AjaxFormMixin, FormView):

	template_name = "registration/sign_in.html"
	form_class = AuthForm

	def form_valid(self, form):
		username = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password')
		#attempt to authenticate user
		user = authenticate(self.request, username=username, password=password)
		if user is not None:
			login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
			result = "Success"
			message = 'You are now logged in'
		else:
			message = form_errors(form)
		data = {'result': result, 'message': message}
		return JsonResponse(data)



def sign_out(request):
	logout(request)
	return redirect(reverse('registration:sign-in'))