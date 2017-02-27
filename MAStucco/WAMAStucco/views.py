from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import auth

def home_view(request):
    return render(request, 'home.html', {'page_title': 'Home'})

def workorders_view(request):
    return render(request, 'workorders.html', {'page_title': 'Work Orders'})

def reports_view(request):
    return render(request, 'reports.html', {'page_title': 'Reports'})

def workeradministrarion_view(request):
    return render(request, 'workeradministration.html', {'page_title': 'Worker Administration'})

def login_view(request):
    return render(request, 'login.html', {'page_title': 'Login'})

def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, 'Logged out.')
    return HttpResponseRedirect(reverse('login_page'))
