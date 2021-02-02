from django.shortcuts import render
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from django.views.generic.edit import FormView
from django.views.generic import View, CreateView

from .form import UserRegisterForm, LoginForm, UpdatePasswordForm, VerificationForm

from .models import User
from .functions import code_generator

# Create your views here.

class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = '/'

    def form_valid(self, form):
        # generamos codigo
        codigo = code_generator()

        usuario = User.objects.create_user(
            form.cleaned_data['username'], #con el cleaned data recuperamos el valor de los formularios
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            nombres=form.cleaned_data['nombres'],
            apellidos=form.cleaned_data['apellidos'],
            genero=form.cleaned_data['genero'],
            codregistro=codigo
        )
        #enviar codigo al email
        asunto = 'Confirmación de email'
        mensaje = 'Código de verificación: ' + codigo
        email_remitente = 'dani.aguilera87@gmail.com'

        send_mail(asunto, mensaje, email_remitente, [form.cleaned_data['email'],]) #siempre es un array por si se envia a mas de un usuario
        # una vez confirmado redirigir a pantalla de confirmación.

        return HttpResponseRedirect(
            reverse(
                'users_app:user-verification',
                kwargs={'pk': usuario.id}
            )
        )

class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_app:panel')

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )
        login(self.request, user)
        return super(LoginUser, self).form_valid(form)


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'users_app:user-login'
            )
        )

class UpdatePasswordView(LoginRequiredMixin, FormView):
    template_name = 'users/update.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:user-login')
    login_url = reverse_lazy('users_app:user-login')

    def form_valid(self, form):
        usuario = self.request.user # primero verificar el usuario que esta logueado.
        user = authenticate(
            username=usuario.username,
            password=form.cleaned_data['password1'] #autenticamos el usuario
        )
        if user:
            new_password = form.cleaned_data['password2'] # recuperamos el password nuevo
            usuario.set_password(new_password)
            usuario.save()


        logout(self.request)

        return super(UpdatePasswordView, self).form_valid(form)

class CodeVerificationView(FormView):
    template_name = 'users/verification.html'
    form_class = VerificationForm
    success_url = reverse_lazy('users_app:user-login')

    def get_form_kwargs(self): # enviar nuevos pk a nuestro formulario
        kwargs = super(CodeVerificationView, self). get_form_kwargs()
        kwargs.update({
            'pk': self.kwargs['pk'] #guardamos el pk de la url para poder llamarlo desde el form
        })
        return kwargs

    def form_valid(self, form):

        User.objects.filter(
            id=self.kwargs['pk']
        ).update(
            is_active=True # para poner activo el ID de usuario que recogemos de la url
        )

        return super(CodeVerificationView, self).form_valid(form)