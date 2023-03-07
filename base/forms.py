from django import forms


class LoginUserForm(forms.Form):
    name = forms.CharField(label="имя")
    password = forms.CharField(label="пароль")


class RegisterUserForm(forms.Form):
    name = forms.CharField(label="имя")
    password = forms.CharField(label="пароль")

