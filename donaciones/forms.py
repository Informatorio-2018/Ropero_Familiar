from django import forms
from .models import *

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
        fields = ('neighborhood', 'phone', 'adress')


class DetailsDonationForm(forms.ModelForm):
    class Meta:
        model = DetailsDonation
        fields = ('quantity',)


class TicketForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ('ticket_number',)
