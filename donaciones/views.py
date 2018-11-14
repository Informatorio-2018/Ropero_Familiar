from django.shortcuts import render, redirect
from .forms import FamilyForm, DonationForm
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
