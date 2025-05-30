from django import forms
from django.forms import ModelForm, fields, Form
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Producto, PerfilUsuario

class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = ['idprod', 'nomprod', 'descprod', 'precio', 'imagen']

class IniciarSesionForm(Form):
    username = forms.CharField(widget=forms.TextInput(), label="Usuario")
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")
    class Meta:
        fields = ['username', 'password']

# class RegistrarUsuarioForm(UserCreationForm):
#     rut = forms.CharField(max_length=20, required=True, label="Rut")
#     tipousu = forms.CharField(max_length=50, required=True, label="Tipo de usuario", initial='admin')
#     dirusu = forms.CharField(max_length=300, required=True, label="Dirección")
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email', 'tipousu', 'rut', 'dirusu']

#agregado por fernando #######---------inicio---------#########

class RegistrarUsuarioForm(UserCreationForm):
    # Campos adicionales (para PerfilUsuario)
    rut = forms.CharField(
        max_length=20,
        required=True,
        label="RUT",
        widget=forms.TextInput(attrs={
            'placeholder': 'Ej: 12.345.678-9',
            'class': 'form-control'
        })
    )
    TIPO_USUARIO_CHOICES = [
        ('Cliente', 'Cliente'),
    ]

    tipousu = forms.ChoiceField(
        choices=TIPO_USUARIO_CHOICES,
        initial='Cliente',
        required=True,
        label="Tipo de usuario",
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )




    dirusu = forms.CharField(
        max_length=300,
        required=True,
        label="Dirección",
        widget=forms.Textarea(attrs={
            'placeholder': 'Ej: Calle Falsa 123, Depto. 4B, Santiago',
            'rows': 3,
            'class': 'form-control'
        })
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]

    def __init__(self, *args, **kwargs):
        super(RegistrarUsuarioForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Ej: juancho123',
            'class': 'form-control'
        })
        self.fields['first_name'].widget.attrs.update({
            'placeholder': 'Ej: Juan',
            'class': 'form-control'
        })
        self.fields['last_name'].widget.attrs.update({
            'placeholder': 'Ej: Pérez Soto',
            'class': 'form-control'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Ej: juan.perez@email.com',
            'class': 'form-control'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Mínimo 8 caracteres',
            'class': 'form-control'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Repite tu contraseña',
            'class': 'form-control'
        })



#agregado por fernando #######---------FIN---------#########


class PerfilUsuarioForm(Form):
    first_name = forms.CharField(max_length=150, required=True, label="Nombres")
    last_name = forms.CharField(max_length=150, required=True, label="Apellidos")
    email = forms.CharField(max_length=254, required=True, label="Correo")
    rut = forms.CharField(max_length=20, required=False, label="Rut")
    tipousu = forms.CharField(max_length=50, required=True, label="Tipo de usuario")
    dirusu = forms.CharField(max_length=300, required=False, label="Dirección")

    class Meta:
        fields = '__all__'