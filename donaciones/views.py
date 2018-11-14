from django.shortcuts import render, redirect
from .forms import FamilyForm, DonationForm, ReferringForm,FamilyForm_r
from .models import Donation, Family, Neighborhood, Referring

# Create your views here.
def register_family (request):
	form = FamilyForm(request.POST or None)

	if request.method == 'POST':
		if form.is_valid():
			form.save()
			return redirect('home')
	return render(request,'register_family.html',{'form':form})

def home(request):
	return render(request,'home.html',{})

def receive_donation(request):
    form = DonationForm(request.POST or None)
    return render(request, 'receive_donation.html', {'form': form})

def register_referring_f(request):
	form = FamilyForm_r(request.POST or None)

	if request.method == 'POST':
		if form.is_valid():
			ref = form.save(commit=False)
			ref.role = 'r'
			ref.save()
			family = Family.objects.last()
			return redirect('register_referring',id=family.id)
	return render(request,'register_referring.html',{'form':form})

def register_referring(request,id):
	form = ReferringForm(request.POST or None)
	family = Family.objects.get(pk=id)
	if request.method == 'POST':
		if form.is_valid():
			fam = form.save(commit=False)
			fam.family = family
			form.save()
			return redirect('home')
	return render(request,'register_referring.html',{'form':form})