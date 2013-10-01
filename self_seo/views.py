from django.shortcuts import render_to_response
from django.template import RequestContext


def home_page(request):
    ci = RequestContext(request)
    return render_to_response('base.html', {}, ci)

    
def about_page(request):
    ci = RequestContext(request)
    return render_to_response('about.html', {}, ci)


def tools_page(request):
    ci = RequestContext(request)
    return render_to_response('tools.html', {}, ci)

