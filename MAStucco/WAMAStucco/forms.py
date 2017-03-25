from django.forms import ModelForm,  TextInput
from .models import WorkOrder, Job, PartOrder, User
from django import forms


class WorkOrderForm(ModelForm):
    class Meta:
        model = WorkOrder
        fields = ['customer', 'order_by', 'model', 'notes']
        widgets = {
            'customer': TextInput(attrs={'class': 'form-control', 'placeholder': 'Customer...', 'style': 'width:270px;'}),
            'order_by': TextInput(attrs={'class': 'form-control', 'placeholder': 'Order by...', 'style': 'width:270px;'}),
            'model': TextInput(attrs={'class': 'form-control', 'placeholder': 'Model...', 'style': 'width:270px;'}),
            'notes': TextInput(attrs={'class': 'form-control', 'placeholder': 'Notes...', 'style': 'width:270px;'})
        }


class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = ['lot', 'address', 'subdivision']
        widgets = {
            'lot': TextInput(attrs={'class': 'form-control', 'placeholder': 'Lot...', 'style': 'width:270px;'}),
            'address': TextInput(attrs={'class': 'form-control', 'placeholder': 'Address...', 'style': 'width:270px;'}),
            'subdivision': TextInput(attrs={'class': 'form-control', 'placeholder': 'subdivision...', 'style': 'width:270px;'})
        }


class PartOrderForm(ModelForm):
    class Meta:
        model = PartOrder
        fields = ['quantity', 'part', 'measure']
        widgets = {
            'quantity': TextInput(attrs={'class': 'form-control', 'placeholder': 'Quantity...', 'style': 'width:270px;'}),
            'part': TextInput(attrs={'class': 'form-control', 'placeholder': 'Part...', 'style': 'width:270px;'}),
            'measure': TextInput(attrs={'class': 'form-control', 'placeholder': 'Measure...', 'style': 'width:270px;'})
        }


class UserForm(ModelForm):
    class Meta:
        password = forms.CharField(widget=forms.PasswordInput)
        model = User
        fields = ['first_name', 'last_name', 'email','username', 'password']
        widgets = {
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'Username...', 'style': 'width:270px;'}),
            'email': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email...', 'style': 'width:270px;'}),
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name...', 'style': 'width:270px;'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name...', 'style': 'width:270px;'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width:270px;'})
        }
