from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from profile.forms import RegistrationForm, LoginForm
from django.contrib.auth.hashers import (make_password, check_password)

def registration_page(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect( '/dashboard/') 
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, password=password)
            user.set_password(password)
            user.save()
            seo_specialist = user.get_profile()
            seo_specialist.name = form.cleaned_data['name']
            seo_specialist.birthday = form.cleaned_data['birthday']
            seo_specialist.save()
            seo_specialist = authenticate(username=username, password=password)
            login(request, seo_specialist)            
            return HttpResponseRedirect('/dashboard/')
        else:
            return render_to_response('register.html', {'form': form}, RequestContext(request))
    else:
        # user not submitting the registration form so show a blank form 
        form = RegistrationForm()
        context = {}
        context.update(csrf(request))
        context = {'form': form}
        return render_to_response('register.html', context, RequestContext(request))
    
def login_page(request):
    if request.user.is_authenticated(): # if user is already logged in
        return HttpResponseRedirect('/dashboard/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            seo_specialist = authenticate(username=username, password=password)
            if seo_specialist is not None:
                login(request, seo_specialist)
                print 'logged in!'
                return HttpResponseRedirect('/dashboard/')
            else:
                print 'invalid login'
                return render_to_response('login.html', {'form':form}, RequestContext(request))
#                return render(request, 'login.html', {'form': form})
        else:
            return render_to_response('login.html', {'form':form}, RequestContext(request))
#            return render(request, 'login.html', {'form': form})
    else: 
        form = LoginForm()
        context = {'form': form}
        return render_to_response('login.html', {'form':form}, RequestContext(request))
#        return render(request, 'login.html', context)

def dashboard_page(request):
    return render_to_response('dashboard.html')

def logout_request(request):
    logout(request)
    return HttpResponseRedirect('/')

def redirect_profile_to_home(request):
    return HttpResponseRedirect('/')
    
@login_required
def dashboard_page(request):
    if not request.user.is_authenticated(): # double safety check
        return HttpResponseRedirect('/login/')
    seo_specialist = request.user.get_profile()

    context = {'seo_specialist': seo_specialist}
    return render(request, 'dashboard.html', context)



