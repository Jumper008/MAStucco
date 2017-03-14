from django.forms import ModelForm,  TextInput
from .models import WorkOrder, Job, PartOrder


class WorkOrderForm(ModelForm):
    class Meta:
        model = WorkOrder
        fields = ['customer', 'order_by', 'model', 'notes']
        widgets = {
            'customer': TextInput(attrs={'class': 'form-control', 'placeholder': 'Customer...', 'style': 'width:300px;'}),
            'order_by': TextInput(attrs={'class': 'form-control', 'placeholder': 'Order by...', 'style': 'width:300px;'}),
            'model': TextInput(attrs={'class': 'form-control', 'placeholder': 'Model...', 'style': 'width:300px;'}),
            'notes': TextInput(attrs={'class': 'form-control', 'placeholder': 'Notes...', 'style': 'width:300px;'})
        }


class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = ['lot', 'address', 'subdivision']
        widgets = {
            'lot': TextInput(attrs={'class': 'form-control', 'placeholder': 'Lot...', 'style': 'width:300px;'}),
            'address': TextInput(attrs={'class': 'form-control', 'placeholder': 'Address...', 'style': 'width:300px;'}),
            'subdivision': TextInput(attrs={'class': 'form-control', 'placeholder': 'subdivision...', 'style': 'width:300px;'})
        }


class PartOrderForm(ModelForm):
    class Meta:
        model = PartOrder
        fields = ['quantity', 'part', 'measure']
        widgets = {
            'quantity': TextInput(attrs={'class': 'form-control', 'placeholder': 'Quantity...', 'style': 'width:300px;'}),
            'part': TextInput(attrs={'class': 'form-control', 'placeholder': 'Part...', 'style': 'width:300px;'}),
            'measure': TextInput(attrs={'class': 'form-control', 'placeholder': 'Measure...', 'style': 'width:300px;'})
        }