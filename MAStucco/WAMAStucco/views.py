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

def login_view(request):
    return render(request, 'login.html', {'page_title': 'Login'})
