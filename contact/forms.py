from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField(label=(u'Subject'), required=True)
    email = forms.EmailField(label=(u'Email'), required=True)
    message = forms.CharField(label=(u'Message'), widget=forms.Textarea, required=True)
