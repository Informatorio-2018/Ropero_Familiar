from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.db.models import Q, Sum
from django.contrib.auth import authenticate, login as log, logout as logout_django
from django.contrib.auth.decorators import login_required


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
    details = DetailsDonation.objects.filter(donation__pk=donator.id)
    if request.method == 'POST':
        form_details = DetailsDonationForm(request.POST)
        form_others = OtherDetailForm(request.POST)
        if form_details.is_valid():
            detail = form_details.save(commit=False)
            detail.donation_type = request.POST['donation_type']
            detail.unit_measure = request.POST['unit_measure']
            detail.donation_id = donator.id
            detail.save()
            if detail.donation_type == 'Otros':
                if form_others.is_valid():
                    other = form_others.save(commit=False)
                    other.detailsdonation_id = detail.id
                    other.save()

            type_sum = TypesDonation.objects.get(name=detail.donation_type)
            if detail.donation_type == type_sum.name:
                type_sum.quantity_total += detail.quantity
                type_sum.save()
            return redirect('items_donation', id=id)
    else:
        form_details = DetailsDonationForm()
        form_others = OtherDetailForm()
    context = {'donator': donator, 'types': types,
               'form_details': form_details, 'details': details, 'form_others': form_others}
    return render(request, 'items_donation.html', context)


def resume_donation(request, id):
    donator = Donation.objects.get(pk=id)
    detail = DetailsDonation.objects.filter(donation__pk=id)
    if request.method == "POST":
        if 'edit_donator' in request.POST:
            don_form = DonationForm(request.POST, instance=donator)
            if don_form.is_valid():
                don_form.save()
                return redirect('resume_donation', id=donator.id)
        elif 'edit_quantity' in request.POST:
            quan_form = DetailsDonationForm(request.POST)
            if quan_form.is_valid():
                quan_form.save()
                return redirect('resume_donation', id=donator.id)
    else:
        don_form = DonationForm(instance=donator)
        quan_form = DetailsDonationForm()
    context = {'donator': donator, 'resumes': DetailsDonation.objects.filter(donation__pk=id), 'don_form': don_form, 'quan_form': quan_form}
    return render(request, 'resume_donation.html', context)


def delete_donation(request, id):
    detail = get_object_or_404(DetailsDonation, pk=id)
    id_donator = detail.donation_id
    types = TypesDonation.objects.all()
    type_res = TypesDonation.objects.get(name=detail.donation_type)
    if detail.donation_type == type_res.name:
        type_res.quantity_total -= detail.quantity
        type_res.save()
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


def register_referring_f(request):
    form = FamilyForm_r(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            ref = form.save(commit=False)
            ref.role = 'r'
            ref.birth = request.POST['birth']
            ref.save()
            family = Family.objects.last()
            return redirect('/registrar_referente_f/'+str(ref.id)+'/')
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
            return redirect('/busqueda_referente/')
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
    types = TypesProducts.objects.all()
    if request.method == 'POST':
        form = SortProductForm(request.POST)
        if form.is_valid():
            sort = form.save(commit=False)

            sort.types_id = request.POST['types_id']
            sort.save()
            return redirect('sort_products')

    else:
        form = SortProductForm()
    context = {'types': types, 'form': form}
    return render(request, 'sort_products.html', context)


def register_family(request, id):
    form = FamilyForm(request.POST or None)
    # import ipdb; ipdb.set_trace()
    if request.method == 'POST':
        if form.is_valid():
            fam = form.save(commit=False)
            fam.ref = id
            fam.role = 'f'
            fam.birth = request.POST['birth']
            fam.save()
            return redirect('/referente/'+str(id)+'/familiares/')
    return render(request, 'register_family.html', {'form': form})


def referring_search(request):
    ref = Referring.objects.all()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            q1 = Q(family__firstname__contains=query)
            q2 = Q(family__lastname__contains=query)
            ref = Referring.objects.filter(q1 | q2)
            return render(request, 'referring_search_out.html', {'ref': ref,
                                                                 'query': query})
    else:
        form = SearchForm()
    return render(request, 'referring_search.html', {'form': form,
                                                     'ref': ref})


def referring_profile(request, id):
    ref = Referring.objects.get(family_id=id)
    return render(request, 'referring_profile.html', {'ref': ref})


def referring_relatives(request, id):
    ref = Family.objects.get(pk=id)
    fam = Family.objects.filter(ref=id)
    return render(request, 'referring_relatives.html', {'ref': ref,
                                                        'fam': fam})

def relative_profile(request,id):
    fam = Family.objects.get(pk=id)
    return render(request, 'relative_profile.html', {'fam': fam})


@login_required
def home(request):
    return render(request, 'home.html', {})

def edit_referring(request,id):
    family = Family.objects.get(pk=id)
    neigh = Neighborhood.objects.all()
    ref = Referring.objects.get(family_id=id)
    if request.method == 'POST':
        form1 = FamilyForm_r(request.POST, instance=family)
        if form1.is_valid():
            form1.save()
            form2 = ReferringForm(request.POST, instance=ref)
            if form2.is_valid():
                fam = form2.save(commit=False)
                fam.family = family
                fam.neighborhood_id = request.POST['neigh_id']
                fam.save()
            return redirect('referring_profile', id)
    else:
        form1 = FamilyForm_r(instance=family)
        form2 = ReferringForm(instance=ref)
    return render(request,'edit_referring.html',{'form1':form1,
                                                 'form2':form2,
                                                 'neigh': neigh,
                                                 'ref':ref})

def neigh(request):
    neigh = Neighborhood.objects.all()
    if request.method == 'POST':
        form = NeighForm(request.POST)
        if form.is_valid():
            form.save()
    form = NeighForm()
    return render(request, 'neigh.html', {'form': form,
                                          'neigh': neigh})

def edit_neigh(request,id):
    neigh = Neighborhood.objects.get(pk=id)
    if request.method == 'POST':
        form = EditNeighForm(request.POST, instance=neigh)
        if form.is_valid():
            form.save()
            return redirect('neigh')
    form = EditNeighForm(instance=neigh)
    return render(request,'edit_neigh.html',{'form':form,
                                             'neigh':neigh})

def del_neigh(request, id):
    neigh = get_object_or_404(Neighborhood, pk=id)
    neigh.delete()
    return redirect('neigh')


def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            log(request,user)
            return redirect('home')
    form = LoginForm()
    return render(request,'login.html',{'form': form})

@login_required
def logout(request):
    logout_django(request)
    return redirect('login')

def closet(request):
    ref = Referring.objects.all()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            q1 = Q(family__firstname__contains=query)
            q2 = Q(family__lastname__contains=query)
            ref = Referring.objects.filter(q1 | q2)
            return render(request, 'closet_search_out.html', {'ref': ref,
                                                              'query': query})
    else:
        form = SearchForm()
    return render(request,'closet.html',{'form':form,
                                         'ref':ref})

def entry_ok(request,id):
    ref = Referring.objects.get(pk=id)
    
    return render(request,'entry_ok.html',{'ref':ref})