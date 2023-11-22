import re
import bcrypt
from django import forms
from django.utils.safestring import mark_safe
from django.forms import widgets
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()

class NameWidget(widgets.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        attrs = {"class": "form-style", "placeholder": "Your Full Name", "autocomplete": "off"}
        return mark_safe(u'''<i class="input-icon uil uil-user"></i>%s''' % (super(NameWidget, self).render(name, value, attrs)))

class UsernameWidget(widgets.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        attrs = {"class": "form-style", "placeholder": "Your Username", "autocomplete": "off"}
        return mark_safe(u'''<i class="input-icon uil uil-at"></i>%s''' % (super(UsernameWidget, self).render(name, value, attrs)))

class PasswordWidget(widgets.PasswordInput):
    def render(self, name, value, attrs=None, renderer=None):
        attrs = {"class": "form-style", "type": "password", "placeholder": "Your Password", "autocomplete": "off"}
        return mark_safe(u'''<i class="input-icon uil uil-lock-alt"></i>%s''' % (super(PasswordWidget, self).render(name, value, attrs)))

class SignupForm(forms.ModelForm):
    signup = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = User
        fields = ['name', 'username', 'password', 'signup']
        widgets = {
                'name': NameWidget(),
                'username': UsernameWidget(),
                'password': PasswordWidget()
            }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def clean(self):
        
        if 'username' in self.cleaned_data:
            username = self.cleaned_data['username']
            user = User.objects.filter(username=username)

            if user.exists():
                self.add_error('username', 'This username already exists')
            elif len(re.findall('^(?=.{1,20}$)(?![0-9_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$', username)) == 0:
                self.add_error('username', 'Invalid username')

        if 'password' in self.cleaned_data:
            password = self.cleaned_data['password']
            if not password or len(password) <= 8:
                self.add_error('password', 'Password must be longer than 8 digit')



class LoginForm(forms.Form):
    username = forms.CharField(widget=UsernameWidget, max_length=100)
    password = forms.CharField(widget=PasswordWidget, max_length=100)
    login = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    def clean(self):

        if 'username' in self.cleaned_data:
            username = self.cleaned_data['username'] 
            user = User.objects.filter(username=username)

            if not user.exists():
                self.add_error('username', 'This username doesn\'t exists')
