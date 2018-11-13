from django import forms
from .models import Family, Donation


class FamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = '__all__'


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ('name',)
