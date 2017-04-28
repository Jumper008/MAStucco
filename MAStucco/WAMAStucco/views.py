from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from datetime import datetime
from .models import WorkOrder, Job, PartOrder, User, Profile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
import re
from django.db.models import Q
from django.http import HttpResponseRedirect
from .forms import WorkOrderForm, JobForm, PartOrderForm, UserCreationForm, UserChangeForm, UserProfileForm
from django.utils import timezone
from django.forms import formset_factory
from django.forms.models import inlineformset_factory
from django.http import HttpResponse
import xlwt
import datetime
from django.db import transaction


def user_check(user):
    return user.is_staff

def empty_view(request):
    return HttpResponseRedirect(reverse('home_page'))


@login_required()
def home_view(request):
    if request.method == 'POST' and request.POST['search_title'].strip():
        query_string = request.POST['search_title']
        category_query1 = get_query(query_string, ['customer'])

        if request.user.is_staff:
            found_category = WorkOrder.objects.all().exclude(work_phase=WorkOrder.FINISHED).filter(category_query1)
        else:
            found_category = WorkOrder.objects.all().filter(assigned_worker=request.user).filter(category_query1)

        if not found_category:
            return render(request, 'home.html', {'page_title': 'Home', 'is_search_empty': True})
        else:
            return render(request, 'home.html', {'page_title': 'Home', 'work_orders': found_category})

    else:
        if request.user.is_staff:
            found_category = WorkOrder.objects.all().exclude(work_phase=WorkOrder.FINISHED)
        else:
            found_category = WorkOrder.objects.all().filter(assigned_worker=request.user)

        paginator = Paginator(found_category, 5)  # Show 5 contacts per page
        page = request.GET.get('page')
        try:
            found_category1 = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            found_category1 = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            found_category1 = paginator.page(paginator.num_pages)
        return render(request, 'home.html', {'page_title': 'Home', 'work_orders': found_category1})


@login_required()
def orderinput_view(request):
    if request.user.is_staff:
        sub_sub_form_set = formset_factory(PartOrderForm, extra=5)
        if request.method == 'POST':
            form = WorkOrderForm(request.POST)
            sub_form = JobForm(request.POST)
            formset_part = sub_sub_form_set(request.POST)
            if form.is_valid() and sub_form.is_valid():
                a = form.save(commit=False)
                a.is_cashed = False
                a.is_taken = False
                a.work_phase = 'CU'
                #a.assigned_worker = request.user
                a.date = timezone.now()
                a.save()
                b = sub_form.save(commit=False)
                b.work_order = a
                b.save()
                if formset_part.is_valid():
                    for form_part in formset_part:
                        c = form_part.save(commit=False)
                        c.work_order = a
                        if c.part != '':
                            c.save()

                messages.success(request, 'Added a new work order successfully')
                return HttpResponseRedirect(reverse('home_page'))
        else:
            form = WorkOrderForm()
            sub_form = JobForm()
            #sub_sub_form = PartOrderForm()

        return render(request, 'order_input.html', {'form': form, 'sub_form': sub_form, 'formset': sub_sub_form_set()})

    else:
        messages.error(request, 'You are not authorized to access this area')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



@login_required()
def workorders_view(request):
    if request.method == 'POST' and request.POST['search_title'].strip():
        query_string = request.POST['search_title']
        category_query1 = get_query(query_string, ['customer'])

        # --Check position--
        if request.user.profile.position == 'NA':
            found_category = WorkOrder.objects.all().filter(is_taken=False).exclude(work_phase=WorkOrder.FINISHED)\
                .filter(category_query1)
        elif request.user.profile.position == 'CU':
            found_category = WorkOrder.objects.all().filter(is_taken=False).exclude(work_phase=WorkOrder.FINISHED) \
                .exclude(work_phase=WorkOrder.MOULDING).exclude(work_phase=WorkOrder.INSTALLING) \
                .filter(category_query1)
        elif request.user.profile.position == 'MO':
            found_category = WorkOrder.objects.all().filter(is_taken=False)\
                .filter(work_phase=WorkOrder.MOULDING).filter(category_query1)
        elif request.user.profile.position == 'IN':
            found_category = WorkOrder.objects.all().filter(is_taken=False)\
                .filter(work_phase=WorkOrder.INSTALLING).filter(category_query1)
        # ----------------------------------

        if not found_category:
            return render(request, 'workorders.html', {'page_title': 'Work Orders', 'is_search_empty': True})
        else:
            return render(request, 'workorders.html',
                          {'page_title': 'Work Orders', 'work_orders': found_category})

    else:

        # --Check position--
        if request.user.profile.position == 'NA':
            found_category = WorkOrder.objects.all().filter(is_taken=False).exclude(work_phase=WorkOrder.FINISHED)
        elif request.user.profile.position == 'CU':
            found_category = WorkOrder.objects.all().filter(is_taken=False).exclude(work_phase=WorkOrder.FINISHED) \
                .exclude(work_phase=WorkOrder.MOULDING).exclude(work_phase=WorkOrder.INSTALLING)
        elif request.user.profile.position == 'MO':
            found_category = WorkOrder.objects.all().filter(is_taken=False).filter(work_phase=WorkOrder.MOULDING)
        elif request.user.profile.position == 'IN':
            found_category = WorkOrder.objects.all().filter(is_taken=False).filter(work_phase=WorkOrder.INSTALLING)
        # ----------------------------------

        paginator = Paginator(found_category, 5)  # Show 25 contacts per page
        page = request.GET.get('page')
        try:
            found_category1 = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            found_category1 = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            found_category1 = paginator.page(paginator.num_pages)
        return render(request, 'workorders.html',
                      {'page_title': 'Work Orders', 'work_orders': found_category1})


@login_required()
@user_passes_test(user_check)
def reports_view(request):
    uncashed_work_orders = WorkOrder.objects.all().filter(is_cashed= False, work_phase=WorkOrder.FINISHED)
    if request.method == 'POST' and request.POST['search_title'].strip():
        query_string = request.POST['search_title']
        category_query1 = get_query(query_string, ['customer'])
        found_category = WorkOrder.objects.all().filter(is_cashed= False,
                                                        work_phase=WorkOrder.FINISHED).filter(category_query1)
        if not found_category:
            return render(request, 'reports.html', {'page_title': 'Reports', 'is_search_empty': True})
        else:
            return render(request, 'reports.html', {'page_title': 'Reports', 'uncashed_work_orders': found_category})

    else:
        found_category = WorkOrder.objects.all().filter(is_cashed=False, work_phase=WorkOrder.FINISHED)
        paginator = Paginator(found_category, 5)  # Show 25 contacts per page
        page = request.GET.get('page')
        try:
            found_category1 = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            found_category1 = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            found_category1 = paginator.page(paginator.num_pages)
        return render(request, 'reports.html', {'page_title': 'Reports', 'uncashed_work_orders': found_category1})


def reports_cashed_view(request):
    cashed_work_orders = WorkOrder.objects.all().filter(is_cashed=True, work_phase=WorkOrder.FINISHED)
    if request.method == 'POST' and request.POST['search_title'].strip():
        query_string = request.POST['search_title']
        category_query1 = get_query(query_string, ['customer'])
        found_category = WorkOrder.objects.all().filter(is_cashed= True,
                                                        work_phase=WorkOrder.FINISHED).filter(category_query1)
        if not found_category:
            return render(request, 'reports_cashed.html', {'page_title': 'Reports', 'is_search_empty': True})
        else:
            return render(request, 'reports_cashed.html', {'page_title': 'Reports', 'cashed_work_orders': found_category})

    else:
        found_category = WorkOrder.objects.all().filter(is_cashed=True, work_phase=WorkOrder.FINISHED)
        paginator = Paginator(found_category, 5)  # Show 25 contacts per page
        page = request.GET.get('page')
        try:
            found_category1 = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            found_category1 = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            found_category1 = paginator.page(paginator.num_pages)
        return render(request, 'reports_cashed.html', {'page_title': 'Reports', 'cashed_work_orders': found_category1})

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    # Splits the query string in individual keywords, getting rid of unnecessary spaces and grouping quoted words
    #   together.
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    # Returns a query, that is a combination of Q objects. That combination aims to search keywords within a model by
    #   testing the given search fields.
    query = None  # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None  # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

@login_required()
def workorder_view(request, id):
    # Validate that the specified work order exists and if so, get it.
    if WorkOrder.exists(id):
        work_order = WorkOrder.getByID(id)
    # If it does not exist, then redirect.
    else:
        return HttpResponseRedirect(reverse('reports_page'))

    part_orders = PartOrder.objects.all().filter(work_order=work_order)

    # If this is a POST request then one of the available buttons were used and we need to find out which one was used
    # to know which action to perform.
    if request.method == 'POST':
        if request.user.is_staff:
            work_order.is_cashed = True
            work_order.save()
            messages.success(request, 'Report has been cashed')
        elif work_order.is_taken and work_order.assigned_worker == request.user:
            if work_order.work_phase == 'CU':
                work_order.work_phase = 'MO'
                work_order.assigned_worker = None
            elif work_order.work_phase == 'MO':
                work_order.work_phase = 'IN'
                work_order.assigned_worker = None
            elif work_order.work_phase == 'IN':
                work_order.work_phase = 'FI'

            work_order.is_taken = False
            work_order.save()
            messages.success(request, 'Job has been marked as finished')
        else:
            with transaction.atomic():
                current = User.objects.select_for_update().get(id=request.user.id)
                if(work_order.is_taken != False):
                    messages.error(request, 'Job is not longer available')
                else:
                    work_order.is_taken = True
                    work_order.assigned_worker = request.user
                    work_order.save()
                    messages.success(request, 'Job has been taken')


        return HttpResponseRedirect(reverse('home_page'))
    # Then we'll display all the information of the requested work order.
    return render(request, 'workorder.html', {'page_title': 'Work Order', 'work_order': work_order,
                                              'part_orders': part_orders})

@login_required()
def workeradministration_view(request):
    worker_list = User.objects.all().filter(is_active=True)
    if request.user.is_staff:
        if request.method == 'POST' and request.POST['search_title'].strip():
            query_string = request.POST['search_title']
            category_query1 = get_query(query_string, ['username'])
            found_category = User.objects.all().filter().filter(category_query1)
            if not found_category:
                return render(request, 'workeradministration.html', {'page_title': 'Worker Administration', 'is_search_empty': True})
            else:
                return render(request, 'workeradministration.html', {'page_title': 'Worker Administration', 'worker_list': found_category})

        else:
            found_category = User.objects.all().filter(is_active=True)
            paginator = Paginator(found_category, 5)  # Show 25 workers per page
            page = request.GET.get('page')
            try:
                found_category1 = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                found_category1 = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                found_category1 = paginator.page(paginator.num_pages)
            return render(request, 'workeradministration.html',
                              {'page_title': 'Worker Administration', 'worker_list': found_category1})
    else:
        messages.error(request, 'You are not authorized to access this area')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def workeradministration_unactive_view(request):
    unactive_workers_list = User.objects.all().filter(is_active=False)
    if request.user.is_staff:
        if request.method == 'POST' and request.POST['search_title'].strip():
            query_string = request.POST['search_title']
            category_query1 = get_query(query_string, ['username'])
            found_category = User.objects.all().filter(is_active= False).filter(category_query1)
            if not found_category:
                return render(request, 'workeradministration_unactive.html', {'page_title': 'Worker Administration', 'is_search_empty': True})
            else:
                return render(request, 'workeradministration_unactive.html', {'page_title': 'Worker Administration', 'unactive_workers_list': found_category})

        else:
            found_category = User.objects.all().filter(is_active=False)
            paginator = Paginator(found_category, 5)  # Show 25 workers per page
            page = request.GET.get('page')
            try:
                found_category1 = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                found_category1 = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                found_category1 = paginator.page(paginator.num_pages)
            return render(request, 'workeradministration_unactive.html', {'page_title': 'Worker Administration', 'unactive_workers_list': found_category1})
    else:
        messages.error(request, 'You are not authorized to access this area')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required()
def updateuser_view(request, id):
    obj = get_object_or_404(User, pk=id)
    obj2 = get_object_or_404(Profile, user=id)
    form = UserChangeForm(request.POST or None,
                        request.FILES or None, instance=obj)
    form2 = UserProfileForm(request.POST or None, request.FILES or None, instance=obj2)
    if request.user.is_staff:
        if request.method == 'POST' and 'edit_worker' in request.POST:
            if form.is_valid() and form2.is_valid():
                form.save()
                form2.save()
                messages.success(request, 'Changes saved successfully')
                return HttpResponseRedirect(reverse('workeradministration_page'))
        return render(request, 'edit_worker.html', {'form': form, 'form2': form2})
    else:
        messages.error(request, 'You are not authorized to access this area')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required()
def newworker_view(request):
    if request.user.is_staff:
        if request.method == "POST":
            form = UserCreationForm(request.POST)
            form2 = UserProfileForm(request.POST)
            if form.is_valid() and form2.is_valid():
                a = form.save(commit=False)
                b = form2.save(commit=False)
                a.save()
                b.user = a
                b.save()
                messages.success(request, 'Added a new worker successfully')
                return HttpResponseRedirect(reverse('workeradministration_page'))
        else:
            form = UserCreationForm()
            form2 = UserProfileForm()
        return render(request, 'new_worker.html', {'form': form, 'form2': form2})

    else:
        messages.error(request, 'You are not authorized to access this area')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def export_xls(request, id):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Report_'+id+'_MAStucco.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Work Order')
    work_order = WorkOrder.getByID(id)
    # Sheet header, first row
    col_num = 0
    row_num = 0

    # BordersLeft
    bordersContent = xlwt.Borders()
    bordersContent.bottom = xlwt.Borders.THIN
    bordersContent.top = xlwt.Borders.THIN
    bordersContent.right = xlwt.Borders.MEDIUM
    bordersContent.left = xlwt.Borders.THIN

    # BordersLeft
    borders = xlwt.Borders()
    borders.bottom = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.right = xlwt.Borders.MEDIUM
    borders.left = xlwt.Borders.MEDIUM

    #BordersTitle
    bordersTitle = xlwt.Borders()
    bordersTitle.bottom = xlwt.Borders.MEDIUM
    bordersTitle.top = xlwt.Borders.MEDIUM
    bordersTitle.right = xlwt.Borders.MEDIUM
    bordersTitle.left = xlwt.Borders.MEDIUM

    #ColorTitle
    patternTitle = xlwt.Pattern()
    patternTitle.pattern = xlwt.Pattern.SOLID_PATTERN
    patternTitle.pattern_fore_colour = xlwt.Style.colour_map['orange']

    # ColorSubTitle
    patternSubTitle = xlwt.Pattern()
    patternSubTitle.pattern = xlwt.Pattern.SOLID_PATTERN
    patternSubTitle.pattern_fore_colour = xlwt.Style.colour_map['light_orange']

    # ColorLeft
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = xlwt.Style.colour_map['gray25']

    #AlignmentContent
    alignWrap = xlwt.Alignment()
    alignWrap.horz = xlwt.Alignment.HORZ_RIGHT
    alignWrap.vert = xlwt.Alignment.VERT_TOP
    alignWrap.wrap = xlwt.Alignment.WRAP_AT_RIGHT

    # StyleLeft
    styleLeft = xlwt.XFStyle()
    styleLeft.borders = all
    styleLeft.font.bold = True
    styleLeft.font.italic = True
    styleLeft.borders = borders
    styleLeft.pattern = pattern

    # StyleTitle
    styleTitle = xlwt.XFStyle()
    styleTitle.borders = all
    styleTitle.font.bold = True
    styleTitle.font.italic = True
    styleTitle.borders = bordersTitle
    styleTitle.pattern = patternTitle

    # StyleSubTitle
    styleSubTitle = xlwt.XFStyle()
    styleSubTitle.borders = all
    styleSubTitle.font.bold = True
    styleSubTitle.font.italic = True
    styleSubTitle.borders = bordersTitle
    styleSubTitle.pattern = patternSubTitle


    # StyleContent
    styleContent = xlwt.XFStyle()
    styleContent.borders = bordersContent
    styleContent.alignment = alignWrap

    ws.write(row_num, col_num, 'Work Order', styleTitle)
    ws.write(row_num, col_num+1, '', styleTitle)

    rows = ['Customer', 'Phase', 'Worker', 'Date', 'Order By', 'Model', 'Notes']

    for row in range(len(rows)):
        ws.write(row_num+row+1, col_num, rows[row], styleLeft)
        ws.col(col_num).width = 256 * 15

    # Sheet body, remaining rows
    #work_order = WorkOrder.getByID(49)
    col_num += 1

    ws.write(row_num+1, col_num, work_order.customer, styleContent)
    ws.write(row_num+2, col_num, work_order.work_phase, styleContent)
    ws.write(row_num+3, col_num, work_order.assigned_worker.first_name + ' ' + work_order.assigned_worker.last_name, styleContent)
    ws.write(row_num + 4, col_num, work_order.date.strftime('%d, %b %Y'), styleContent)
    ws.write(row_num+5, col_num, work_order.order_by, styleContent)
    ws.write(row_num+6, col_num, work_order.model, styleContent)
    ws.write(row_num+7, col_num, work_order.notes, styleContent)
    ws.col(col_num).width = 256 * 40

    col_num -= 1
    row_num += 10

    ws.write(row_num, col_num, 'Part Orders', styleTitle)
    ws.write(row_num , col_num + 1, '', styleTitle)

    part_orders = PartOrder.objects.all().filter(work_order=work_order)

    rows = ['Quantity', 'Part', 'Measure']
    cont=0
    for part in part_orders:
        cont+=1
        ws.write(row_num + 1, col_num,'', styleSubTitle)
        ws.write(row_num +1 , col_num+1, '', styleSubTitle)
        row_num += 1
        for row in range(len(rows)):
            ws.write(row_num + row + 1, col_num, rows[row], styleLeft)
            ws.col(col_num).width = 256 * 15

        col_num += 1
        ws.write(row_num + 1, col_num, part.quantity, styleContent)
        ws.write(row_num + 2, col_num, part.part, styleContent)
        ws.write(row_num + 3, col_num, part.measure, styleContent)
        col_num -= 1
        row_num += 3

    row_num += 3

    ws.write(row_num, col_num, 'Job Information', styleTitle)
    ws.write(row_num , col_num + 1, '', styleTitle)

    rows = ['Lot', 'Address', 'Subdivision']

    for row in range(len(rows)):
        ws.write(row_num + row + 1, col_num, rows[row], styleLeft)
        ws.col(col_num).width = 256 * 15

    col_num += 1
    ws.write(row_num+1, col_num, work_order.job.lot, styleContent)
    ws.write(row_num+2, col_num, work_order.job.address, styleContent)
    ws.write(row_num+3, col_num, work_order.job.subdivision, styleContent)

    wb.save(response)
    return response


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
            nextTo = None
    else:
        nextTo = request.GET.get('next', None)

    return render(request, 'login.html', {'page_title': 'Login', 'next': nextTo})

def logout_view(request):
    logout(request)
    #messages.success(request, 'Successfully logged out')
    return HttpResponseRedirect(reverse('login_page'))