from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from datetime import datetime

# Validators:

# Class Models:
class WorkOrder(models.Model):

    date = models.DateTimeField()
    customer = models.CharField\
        (
            max_length=128
        )
    order_by = models.CharField\
        (
            max_length=128
        )
    model = models.CharField\
        (
            max_length=128
        )
    is_cashed = models.BooleanField()
    is_taken = models.BooleanField()
    ADDED = 'AD'
    CUTTING = 'CU'
    MOULDING = 'MO'
    INSTALLING = 'IN'
    FINISHED = 'FI'
    work_phase = models.CharField\
        (
            max_length=2,
            default=ADDED
        )
    notes = models.CharField\
        (
            max_length=256
        )
    assigned_worker = models.ForeignKey\
        (
            User,
            related_name='work_orders',
            related_query_name='work_order'
        )

    @classmethod
    def exists(cls, id):
        return len(cls.objects.filter(pk=id)) > 0

    @classmethod
    def getByID(cls, id):
        return cls.objects.get(pk=id)

    def __str__(self):
        return str(self.customer)

    def __unicode__(self):
        return str(self.customer)

    class Meta:
        ordering = ['-date']

class WorkOrderForm(ModelForm):
    class Meta:
        model = WorkOrder
        fields = ['customer', 'order_by', 'model', 'notes']

class PartOrder(models.Model):

    quantity = models.PositiveIntegerField()
    part = models.CharField\
        (
            max_length=128
        )
    measure = models.CharField\
        (
            max_length=128
        )
    work_order = models.ForeignKey\
        (
            WorkOrder,
            on_delete=models.CASCADE,
            related_name='part_orders',
            related_query_name='part_order'
        )

    @classmethod
    def exists(cls, id):
        return len(cls.objects.filter(pk=id)) > 0

    @classmethod
    def getByID(cls, id):
        return cls.objects.get(pk=id)

    def __str__(self):
        return str(self.part)

    def __unicode__(self):
        return str(self.part)

class PartOrderForm(ModelForm):
    class Meta:
        model = PartOrder
        fields = ['quantity', 'part', 'measure']

class Job(models.Model):

    lot = models.BigIntegerField()
    address = models.CharField\
        (
            max_length=256
        )
    subdivision = models.CharField\
        (
            max_length=256
        )
    work_order = models.OneToOneField\
        (
            WorkOrder,
            related_name='job',
            related_query_name='job'
        )

    @classmethod
    def exists(cls, id):
        return len(cls.objects.filter(pk=id)) > 0

    @classmethod
    def getByID(cls, id):
        return cls.objects.get(pk=id)

    def __str__(self):
        return str(self.lot) + str(self.subdivision)

    def __unicode__(self):
        return str(self.lot) + str(self.subdivision)

    class Meta:
        unique_together = ('lot', 'subdivision')

class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = ['lot', 'address', 'subdivision']