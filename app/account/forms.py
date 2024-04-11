from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Insert your name here',
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Insert your password here',
    }))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            qs = User.objects.filter(username=username)
            if not qs.exists():
                raise forms.ValidationError('No such user')
            if not check_password(password, qs[0].password):
                raise forms.ValidationError('Incorrect password')
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Inactive account')
        return super().clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Insert your name here',
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Insert your password here',
    }))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Re-type password',
    }))

    class Meta:
        model = User
        fields = ('username',)

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise ValidationError('Passwords do not match')
        return data['password2']
