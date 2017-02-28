from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import auth


@login_required()
def home_view(request):
    return render(request, 'home.html', {'page_title': 'Home'})


def workorders_view(request):
    return render(request, 'workorders.html', {'page_title': 'Work Orders'})


def reports_view(request):
    return render(request, 'reports.html', {'page_title': 'Reports'})


def workeradministrarion_view(request):
    return render(request, 'workeradministration.html', {'page_title': 'Worker Administration'})


def login_view(request):
    if request.method == 'POST':
        # We get POST arguments.
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        nextTo = request.POST.get('next', reverse('home_page'))
        if nextTo == 'None':
            nextTo = None
        user = auth.authenticate(username=username, password=password)

        if user is not None and user.is_active:
            auth.login(request, user)
            if nextTo is None:
                nextTo = reverse('home_page')
            return HttpResponseRedirect(nextTo)
    else:
        nextTo = request.GET.get('next', None)

    return render(request, 'login.html', {'page_title': 'Login', 'next': nextTo})


def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, 'Logged out.')
    return HttpResponseRedirect(reverse('login_page'))
