from django import forms
from django.contrib.auth.models import User
from site_auditor.models import Site, SEOSpecialist

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(label=(u'Username:'), required=True)
#    email = forms.EmailField(label=(u'Email'), required=True)
    password = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False), required=True)
    password_repeat = forms.CharField(label=(u'Verify password'), widget=forms.PasswordInput(render_value=False), required=True)
#    birthday = forms.DateField(label=(u'Birthday'), required=True, input_formats=['%m/%d/%Y'])
#    name = forms.CharField(label=(u'Full name'), required=True)
    class Meta:
        model = SEOSpecialist
        fields = ['email', 'name', 'birthday']

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password', None)
        password_repeat = cleaned_data.get('password_repeat', None)
        if password and password_repeat and password != password_repeat:
            raise forms.ValidationError('The passwords did not match. Please try again.')
        return cleaned_data
        
"""
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('That username is already taken. Please select another.')
"""
     
""" BUGGY
    def clean_password(self):
        password = self.cleaned_data.get('password', None)
        password_repeat = self.cleaned_data.get('password_repeat', None)
        if password and password_repeat and password != password_repeat:
            raise forms.ValidationError('The passwords did not match. Please try again.')
        return password
"""

class LoginForm(forms.Form):
    username = forms.CharField(label=(u'Username'))
    password = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))