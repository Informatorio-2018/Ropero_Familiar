from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import datetime


class FamilyForm_r(forms.ModelForm):
    class Meta:
        model = Family
        fields = ('firstname', 'lastname', 'dni', 'birth')


class FamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = ('firstname', 'lastname', 'dni', 'birth')


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ('name',)


class ReferringForm(forms.ModelForm):
    class Meta:
        model = Referring
        fields = ('phone', 'adress')


class LoadTypesDonationForm(forms.ModelForm):
    class Meta:
        model = TypesDonation
        fields = ('name', 'unit_measure')


class DetailsDonationForm(forms.ModelForm):
    class Meta:
        model = DetailsDonation
        fields = ('quantity',)


class OtherDetailForm(forms.ModelForm):
    class Meta:
        model = OtherDetail
        fields = ('description',)


class TicketForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ('ticket_number',)


class LoadTypeProductForm(forms.ModelForm):
    class Meta:
        model = TypesProducts
        fields = ('price',)


class SortProductForm(forms.ModelForm):

    class Meta:
        model = SortProducts
        fields = ('types', 'quantity',)


class FixProductForm(forms.ModelForm):
    class Meta:
        model = FixProducts
        fields = ('types', 'quantity',)

        # CHOICES=TypesDonation.objects.all()
        # model = FixProducts
        # fields = ('name','quantity',)
        # widgets={'name':forms.Select(choices=( (x.name, x.name) for x in CHOICES ))}


class ResponsableForm(forms.ModelForm):
    class Meta:
        model = ResponsableFix
        fields = ('name', 'lastname', 'phone', 'adress',)


class CarryForm(forms.ModelForm):
    class Meta:
        model = Carry
        fields = ('quantity',)


class SearchForm(forms.Form):
    query = forms.CharField(label='Búsqueda')


class NeighForm(forms.ModelForm):
    class Meta:
        model = Neighborhood
        fields = ('name',)


class EditNeighForm(forms.ModelForm):
    class Meta:
        model = Neighborhood
        fields = ('name',)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, label='Nombre de Usuario')
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(), label='Contraseña')


class UserRegisterForm(UserCreationForm):
    # phone_number = forms.IntegerField(label='Número de telefono')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'is_staff')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        username = username.upper()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('Ya existe un usuario con este nombre')
        return username


class DonationsReportForm(forms.Form):
    donation = forms.CharField(label='Donaciones')
    begin = forms.DateField(label='Desde', required=False)
    finish = forms.DateField(label='Hasta', required=False)


class SalesDetailsForm(forms.ModelForm):
    class Meta:
        model = SalesDetails
        fields = ('quantity',)


class TotalForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ('total',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # username = username.upper()
        if len(str(phone_number)) != 10:
            raise forms.ValidationError('Número de telefono no valido')
        return phone_number


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'image']
