from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
from contact.forms import ContactForm
from django.http import HttpResponseRedirect
from django.core.mail import send_mail


def contact_page(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(
                cd['subject'],
                cd['message'],
                cd.get('email', 'noreplyg@gmail.com'),
                ['hawooksong@gmail.com'],
            )
            return HttpResponseRedirect('/contact/thanks/')
    else:
        form = ContactForm(
            initial = {'subject': 'I love your site!', 'email': 'your@email.com'}
        )
        context = {'form': form}
        return render(request, 'contact.html', context)


def thanks_page(request):
    return render_to_responsel('thanks.html')

