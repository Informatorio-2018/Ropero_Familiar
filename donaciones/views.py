from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *

# Create your views here.


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
    if request.method == 'POST':
        form = DetailsDonationForm(request.POST)
        if form.is_valid():
            detail = form.save(commit=False)
            detail.donation_type = request.POST['donation_type']
            detail.unit_measure = request.POST['unit_measure']
            detail.donation_id = donator.id
            detail.save()
            return redirect('items_donation', id=id)
    else:
        form = DetailsDonationForm()
    context = {'donator': donator, 'types': types, 'form': form}
    return render(request, 'items_donation.html', context)


def resume_donation(request, id):
    donator = Donation.objects.get(pk=id)
    context = {'donator': donator, 'resumes': DetailsDonation.objects.filter(donation__pk=id)}
    return render(request, 'resume_donation.html', context)


def delete_donation(request, id):
    detail = get_object_or_404(DetailsDonation, pk=id)
    id_donator = detail.donation_id
    detail.delete()
    return redirect('resume_donation', id=id_donator)


def finish_donation(request, id):
    donator = Donation.objects.get(pk=id)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=donator)
        if form.is_valid():
            donator.ticket_number = request.POST['ticket_number']
            donator.save()
            return redirect('receive_donation')
    else:
        form = TicketForm()
    context = {'donator': donator, 'form': form}
    return render(request, 'finish_donation.html', context)

# Facu


def register_referring_f(request):
    form = FamilyForm_r(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            ref = form.save(commit=False)
            ref.role = 'r'
            ref.birth = request.POST['birth']
            ref.save()
            family = Family.objects.last()
            return redirect('register_referring', id=family.id)
    return render(request, 'register_referring_f.html', {'form': form})


def register_referring(request, id):
    form = ReferringForm(request.POST or None)
    family = Family.objects.get(pk=id)
    neigh = Neighborhood.objects.all()
    if request.method == 'POST':
        if form.is_valid():
            fam = form.save(commit=False)
            fam.family = family
            fam.neighborhood_id = request.POST['neigh_id']
            form.save()
            return redirect('home')

    return render(request, 'register_referring.html', {'form': form,
                                                       'neigh': neigh})


def load_types_donation(request):
    if request.method == 'POST':
        form = LoadTypesDonationForm(request.POST)
        if form.is_valid():
            form.save()

    form = LoadTypesDonationForm()
    return render(request, 'load_types_donation.html', {'form': form})


def load_types_products(request):
    if request.method == 'POST':
        form = LoadTypeProductForm(request.POST)
        if form.is_valid():
            form.save()

    form = LoadTypeProductForm()
    return render(request, 'load_types_product.html', {'form': form})


def sort_products(request):
    if request.method == 'POST':
        form = SortProductForm(request.POST)
        if form.is_valid():
            form.save()

    form = SortProductForm()
    return render(request, 'sort_products.html', {'form': form})


def register_family(request):
    form = FamilyForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            fam = form.save(commit=False)
            fam.role = 'f'
            fam.birth = request.POST['birth']
            fam.save()
            return redirect('home')
    return render(request, 'register_family.html', {'form': form})


def home(request):
    return render(request, 'home.html', {})
