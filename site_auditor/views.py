from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
from django.core.context_processors import csrf
from forms import SiteAuditForm
from crawl import *
from django.contrib.auth.decorators import login_required


@login_required
def submit_page(request):
    if request.GET:
        form = SiteAuditForm(request.GET)
        if form.is_valid():
            form.save()
            crawl(request.GET['url'])
            return HttpResponseRedirect('/tools/site_auditor/result/')
    else:
        form = SiteAuditForm()
    context = {}
    context.update(csrf(request))
    context['form'] = form
    return render_to_response('submit.html', context)


@login_required
def result_page(request):
    if request.GET:
        print 'GET GET'
    elif request.POST:
        print 'POST POST'
    else:
        print 'YA YA'
#    print request.GET['url']
#    crawl(request.GET['url'])
    return render_to_response('result.html')


