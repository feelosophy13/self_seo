from django.conf.urls import patterns, include, url 

urlpatterns = patterns('',
    url(r'^site_auditor/$', 'site_auditor.views.submit_page'),
    url(r'^site_auditor/submit/$', 'site_auditor.views.submit_page'),
    url(r'^site_auditor/result/$', 'site_auditor.views.result_page'),   
)
