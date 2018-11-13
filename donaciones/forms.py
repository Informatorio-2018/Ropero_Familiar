from django import forms
from .models import Family, Donation, Referring

class FamilyForm_r(forms.ModelForm):
	class Meta:
		model = Family
		fields = ('firstname','lastname','dni','birth')

class FamilyForm(forms.ModelForm):
	class Meta:
		model = Family
		fields = ('firstname','lastname','dni','birth')

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = '__all__'

class ReferringForm(forms.ModelForm):
	class Meta:
		model = Referring
		fields = ('neighborhood','phone','adress')

