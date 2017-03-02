from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import WorkOrder, Job, PartOrder


@login_required()
def home_view(request):
    pending_work_orders = WorkOrder.objects.all().filter(work_phase=WorkOrder.ADDED)
    return render(request, 'home.html', {'page_title': 'Home', 'work_orders': pending_work_orders})

@login_required()
def workorders_view(request):
    return render(request, 'workorders.html', {'page_title': 'Work Orders'})

@login_required()
def reports_view(request):
    uncashed_work_orders = WorkOrder.objects.all().filter(work_phase=WorkOrder.FINISHED, is_cashed= False)
    cashed_work_orders = WorkOrder.objects.all().filter(work_phase=WorkOrder.FINISHED, is_cashed= True)
    return render(request, 'reports.html', {'page_title': 'Reports', 'uncashed_work_orders': uncashed_work_orders, 'cashed_work_orders':  cashed_work_orders})

@login_required()
def workeradministrarion_view(request):
    return render(request, 'workeradministration.html', {'page_title': 'Worker Administration'})

def login_view(request):
    if request.method == 'POST':
        # We get POST arguments.
        username = request.POST.get('inputUsername', '')
        password = request.POST.get('inputPassword', '')
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