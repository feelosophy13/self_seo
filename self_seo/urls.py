from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^$', 'self_seo.views.home_page'),
    (r'^home/$', 'self_seo.views.home_page'),
    (r'^about/$', 'self_seo.views.about_page'),
    (r'^tools/$', 'self_seo.views.tools_page'),
    (r'^tools/', include('site_auditor.urls')),
    (r'^contact/$', 'contact.views.contact_page'),
    (r'^contact/thanks/$', 'contact.views.thanks_page'),
    (r'^dashboard/$', 'profile.views.dashboard_page'),
    (r'^registration/$', 'profile.views.registration_page'),
    (r'^login/$', 'profile.views.login_page'),
    (r'^logout/$', 'profile.views.logout_request'),
    (r'^dashboard/$', 'profile.views.dashboard_page'),
    (r'^resetpassword/passwordsent/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^resetpassword/$', 'django.contrib.auth.views.password_reset'),
    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    (r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
#    (r'^direct/$', direct_to_template, {'template':'direct.html', 'extra_context':{'s	howDirect': True}}),

#    (r'^accounts/', include('allauth.urls')),
#    (r'^accounts/profile/$', 'site_auditor.views.redirect_profile_to_home'),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
