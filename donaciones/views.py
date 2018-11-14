from django.shortcuts import render, redirect
from .forms import *
from .models import *

# Create your views here.


def register_family(request):
    form = FamilyForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'register_family.html', {'form': form})


def home(request):
    return render(request, 'home.html', {})

# Cristian
def receive_donation(request):
    form = DonationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            donation = Donation.objects.last()
            return redirect('items_donation', id=donation.id)
    context = {'form': form}
    return render(request, 'receive_donations.html', context)


def items_donation(request, id):
    donator = Donation.objects.get(pk=id)
    types = TypesDonation.objects.all()
    context = {'donator': donator, 'types': types}
    return render(request, 'items_donation.html', context)

# Facu
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
