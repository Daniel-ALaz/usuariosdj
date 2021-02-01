from django import forms
from .models import User

class UserRegisterForm(forms.ModelForm):

    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña'
            })
    )

    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repetir contraseña'
            })
    )

    class Meta:

        model = User
        fields = ('username', 'email', 'nombres', 'apellidos', 'genero',)

    def clean_password2(self): #comprobar que las contraseñas son iguales
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'Las contraseñas no coinciden')