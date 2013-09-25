from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from time import time
import datetime
 
class SEOSpecialist(models.Model):
    user = models.OneToOneField(User)
    email = models.EmailField()
    name = models.CharField(max_length=100)
    birthday = models.DateField(null=True)
    def __unicode__(self):
        return self.name

""" BUGGY
def create_user_profile(sender, instance, created, **kwargs):
    if not created:
        SEOSpecialist.objects.create(user=instance)
"""       

def create_user_profile(sender, **kw):
    user = kw["instance"]
    if kw["created"]:
        up = SEOSpecialist(user=user, email=user.email)
        up.save()
post_save.connect(create_user_profile, sender=User)
        
""" WORKING ALTERNATIVE
def create_user_profile(sender, **kw):
    user = kw["instance"]
    if kw["created"]:
        seo_specialist = SEOSpecialist()
        seo_specialist.setUser(sender)
        seo_specialist.save()
post_save.connect(create_user_profile, sender=User)
"""
    
# Create your models here.
class Site(models.Model):
    url = models.URLField(max_length=100)
    canonical_site_set = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.url + ' (' + str(self.created_at) + ')'

class Page(models.Model):
    site = models.ForeignKey(Site)
    url = models.URLField()
    GA_installed = models.BooleanField(blank=True)
    meta_title = models.CharField(max_length=100, blank=True)
    meta_description = models.CharField(max_length=200, blank=True)
    n_incoming_links = models.IntegerField(default=0)
    n_outgoing_links = models.IntegerField(default=0)
    def __unicode__(self):
		return self.url
		
class H_Tag(models.Model):
    text = models.CharField(max_length=130, blank=True)
    site = models.ForeignKey(Site)
    page = models.ForeignKey(Page) 
    level = models.CharField(max_length=2) # h1, h2, h3, h4, h5, h6
    def __unicode__(self):
        return self.text
                
class Image_Link(models.Model):
    link = models.URLField()
    site = models.ForeignKey(Site)
    page = models.ForeignKey(Page)
    alt = models.CharField(max_length=130, blank=True)
    found = models.BooleanField()
    def __unicode__(self):
        return self.link

class CSS_Link(models.Model):
    link = models.URLField()
    site = models.ForeignKey(Site)    
#    page = models.ForeignKey(Page)
    page = models.ManyToManyField(Page)
    found = models.BooleanField()
    def __unicode__(self):
        return self.link
        	
class JS_Link(models.Model):
    link = models.URLField()
    site = models.ForeignKey(Site)
#    page = models.ForeignKey(Page)
    page = models.ManyToManyField(Page)
    found = models.BooleanField()
    def __unicode__(self):
        return self.link
        
class Page_Link(models.Model):
    link = models.URLField()
    site = models.ForeignKey(Site)
#    page = models.ForeignKey(Page)
    page = models.ManyToManyField(Page)
    found = models.BooleanField()
    def __unicode__(self):
        return self.link

class Email_Link(models.Model):
    link = models.URLField()
    site = models.ForeignKey(Site)
#    page = models.ForeignKey(Page)
    page = models.ManyToManyField(Page)
    found = models.BooleanField()
    def __unicode__(self):
        return self.link
        
class External_Link(models.Model):
    link = models.URLField()
    site = models.ForeignKey(Site)
    page = models.ForeignKey(Page)
    found = models.BooleanField()
    def __unicode__(self):
        return self.link
        
class Canonical_Link(models.Model):
    link = models.URLField()
    site = models.ForeignKey(Site)
    page = models.ForeignKey(Page)
    found = models.BooleanField()
    def __unicode__(self):
        return self.link
        
class Trivial_Link(models.Model):
    link = models.URLField()
    site = models.ForeignKey(Site)
    page = models.ForeignKey(Page)
    found = models.BooleanField()
    def __unicode__(self):
        return self.link

class Static_File_Link(models.Model):
    link = models.URLField()
    site = models.ForeignKey(Site)
    page = models.ForeignKey(Page)
    found = models.BooleanField()
    def __unicode__(self):
        return self.link
