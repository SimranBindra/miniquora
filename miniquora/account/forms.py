from django import forms
from django.contrib.auth import authenticate
from .models import CustomUser

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 20)
    password = forms.CharField(widget = forms.PasswordInput(attrs = {'class' : 'dumb', 'placeholder' : 'Enter Password'}))
    def __init__(self, *args, **kwargs):
        self.user_cache = None
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            self.user_cache = authenticate(username = username, password = password)
            if self.user_cache is None:
                raise forms.ValidationError('Invalid username or password')
            elif not self.user_cache.is_active:
                raise forms.ValidationError('User is not Active')
        return self.cleaned_data

    def get_user(self):
        return self.user_cache

class SignupForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget = forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget = forms.PasswordInput, help_text = 'Should be same as Password')
    def clean_password2(self):
        data_password1 = self.cleaned_data['password1']
        data_password2 = self.cleaned_data['password2']
        if data_password1 and data_password2 and data_password1 != data_password2:
            raise forms.ValidationError("Passwords don't match")
        return data_password2
    def save(self, commit = True):
        user = super(SignupForm, self).save(commit = False)
        user.set_password(self.cleaned_data.get('password1'))
        user.is_active = False
        if commit:
            user.save()
        return user
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number']

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(max_length = 254)
    def clean_email(self):
        data_email = self.cleaned_data.get('email')
        if data_email and CustomUser.objects.filter(email = data_email).count() == 0:
            raise forms.ValidationError("We cannot find user with this email address. Please verify email address and try again");
        return data_email

class SetPasswordForm(forms.Form):
    password1 = forms.CharField(label='Password', widget = forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget = forms.PasswordInput, help_text = 'Should be same as Password')
    def clean_password2(self):
        data_password1 = self.cleaned_data['password1']
        data_password2 = self.cleaned_data['password2']
        if data_password1 and data_password2 and data_password1 != data_password2:
            raise forms.ValidationError("Passwords don't match")
        return data_password2
