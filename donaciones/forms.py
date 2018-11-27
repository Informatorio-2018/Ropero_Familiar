from django import forms
from .models import *
from django.contrib.auth.models import User


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
        fields = ('name', 'unit_measure', 'price')


class SortProductForm(forms.ModelForm):
    lista=[]
    control = TypesDonation.objects.filter(quantity_total__gte=0)
    for i in control:
        if i.name == 'Ropa':
            lista.append('Ropa Verano')
            lista.append('Ropa Invierno')
        else:
            lista.append(i.name)



        
    class Meta:
        model = SortProducts
        fields = ('types','quantity',)

        widgets= {
        'types':forms.Select(choices='lista')
        }



class SearchForm(forms.Form):
    query = forms.CharField(label='Búsqueda')

class AddNeighForm(forms.ModelForm):
    class Meta:
        model = Neighborhood
        fields = ('name',)

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 20)
    password = forms.CharField(max_length = 20 , widget = forms.PasswordInput())