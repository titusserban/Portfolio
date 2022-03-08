from urllib import request
from django.conf import settings
from django.shortcuts import redirect
from urllib.parse import urlencode
import requests
import json
import datetime
from django.http import JsonResponse


def is_ajax(self):
    return self.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def recaptcha_validation(token):
    #the API call to reCAPTCHA
    result = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data = {
            "secret": settings.RECAPTCHA_SECRET_KEY,
            "response": token
        }
    )
    return result.json()

def redirect_params(**kwargs):
    url = kwargs.get("url")
    params = kwargs.get("params")
    response = redirect(url)
    if params:
        query_string = urlencode(params)
        response["Location"] += "?" + query_string
    return response

def form_errors(*args):
    #Handle form errors
    message = ""
    for error in args:
        if error.errors:
            message = error.errors.as_text()
    return message


class AjaxFormMixin(object):
    #ajaxify django form
    def form_invalid(self, form):
        message = form_errors(form)
        return JsonResponse({"result": "Error", "message": message})


    def form_valid(self, form):
        form.save()
        return JsonResponse({"result": "Success", "message": ""})





