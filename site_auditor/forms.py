from django import forms
from django.contrib.auth.models import User
from site_auditor.models import Site, SEOSpecialist

class SiteAuditForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ['url'] 
    
    
    
