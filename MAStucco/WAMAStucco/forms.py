from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms import ModelForm, TextInput, Select
from .models import WorkOrder, Job, PartOrder, User, Profile
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


class UserCreationForm(ModelForm):
    username = forms.CharField(help_text=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username...', 'style': 'width:270px;'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width:270px;'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width:270px;'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
        widgets = {
            'email': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email...', 'style': 'width:270px;'}),
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name...', 'style': 'width:270px;'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name...', 'style': 'width:270px;'})
        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError(u'Username "%s" is already in use.' % username)
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        duplicate_users = User.objects.filter(email=email)
        if self.instance.pk is not None:  # If you're editing an user, remove him from the duplicated results
            duplicate_users = duplicate_users.exclude(pk=self.instance.pk)
        if duplicate_users.exists():
            raise forms.ValidationError("Email is already registered.")
        return email

class UserChangeForm(ModelForm):
    username = forms.CharField(help_text=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username...', 'style': 'width:270px;'}))
    is_active = forms.BooleanField(help_text=False)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'is_active']
        widgets = {
            'email': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email...', 'style': 'width:270px;'}),
            'first_name': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'First Name...', 'style': 'width:270px;'}),
            'last_name': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Last Name...', 'style': 'width:270px;'})
        }


class UserProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['position']
        widgets = {
            'position': Select(attrs={'class': 'form-control', 'style': 'width:270px;'})
        }