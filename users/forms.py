from django import forms
from django.contrib.auth import authenticate

from users.models import CustomUser

class UserLoginForm(forms.Form):
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):
        data = self.cleaned_data
        email = data['email']
        password = data['password']
        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Invalid login credentials")
        return data

    def get_user(self):
        return self.user_cache


class UserCreationForm(forms.Form):
    first_name = forms.CharField(label='First name',max_length=150, required=True)
    last_name = forms.CharField(label="Last name", max_length=150, required=False)
    email = forms.EmailField(label='Email', required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput, required=True)

    def clean_password2(self):
        if self.cleaned_data['password2'] != self.cleaned_data['password1']:
            raise forms.ValidationError("Passwords must be equal!")
        return self.cleaned_data['password1']

    def clean_email(self):
        if CustomUser.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("Bu email bilan user ro'yxatdan o'tgan!")
        return self.cleaned_data['email']

    def save(self, commit=True):
        data = self.cleaned_data
        user = CustomUser(first_name=data['first_name'],
                          last_name=data['last_name'],
                          email=data['email'],
                          )
        user.set_password(data['password1'])
        if commit:
            user.save()
        return user


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email", 'image')
