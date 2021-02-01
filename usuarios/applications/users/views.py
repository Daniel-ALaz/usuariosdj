from django.shortcuts import render

from django.views.generic.edit import FormView

from .form import UserRegisterForm

# Create your views here.

class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = '/'