"""MAStucco URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from WAMAStucco import views

urlpatterns = [
    url(r'^$', views.empty_view),
    url(r'^home/$', views.home_view, name='home_page'),
    url(r'^home/info/(?P<id>\d+)$', views.workorder_view),
    url(r'^workorders/$', views.workorders_view, name='workorders_page'),
    url(r'^workorders/order_input$', views.orderinput_view, name='order_input_page'),
    url(r'^reports/$', views.reports_view, name='reports_page'),
    url(r'^reports_cashed/$', views.reports_cashed_view, name='reports_cashed_page'),
    url(r'^reports/info/(?P<id>\d+)$', views.workorder_view),
    url(r'^export/(?P<id>\d+)$', views.export_xls, name='export_xls'),
    url(r'^workeradministration/$', views.workeradministration_view, name='workeradministration_page'),
    url(r'^workeradministration_unactive/$', views.workeradministration_unactive_view, name='workeradministration_unactive_page'),
    url(r'^workeradministration/info/(?P<id>\d+)$', views.updateuser_view, name='edit_worker_page'),
    url(r'^workeradministration/new_worker$', views.newworker_view, name='new_worker_page'),
    url(r'^login/$', views.login_view, name='login_page'),
    url(r'^logout/$', views.logout_view),
    url(r'^admin/', admin.site.urls)
]