from django.shortcuts import render, redirect, get_object_or_404 
from django.http import JsonResponse
from django.contrib import messages
from .forms import *
from .models import *
from django.db.models import Q, Sum, F
from django.contrib.auth import authenticate, login as log, logout as logout_django
from django.contrib.auth.decorators import login_required
from django.utils.timezone import datetime as datetime_django
import datetime
from decimal import Decimal
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.admin.views.decorators import staff_member_required


@login_required
def receive_donation(request):
    form = DonationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            donation = Donation.objects.last()
            return redirect('items_donation', id=donation.id)
    context = {'form': form}
    return render(request, 'receive_donations.html', context)

@login_required
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

@login_required
def resume_donation(request, id):
    # import ipdb; ipdb.set_trace()
    donator = Donation.objects.get(pk=id)
    resumes = DetailsDonation.objects.filter(donation__pk=id)
    if request.method == "POST":
        don_form = DonationForm(request.POST, instance=donator)
        if don_form.is_valid():
            don_form.save()
            return redirect('resume_donation', id=donator.id)
    else:
        don_form = DonationForm(instance=donator)
    context = {'donator': donator, 'resumes': resumes, 'don_form': don_form}
    return render(request, 'resume_donation.html', context)

@login_required
def edit_donation(request, id):
    detail = get_object_or_404(DetailsDonation, pk=id)
    id_donator = detail.donation_id
    types = TypesDonation.objects.all()
    type_edit = types.get(name=detail.donation_type)

    if request.method == 'POST':
        # Resta del total la cantidad a editar
        if detail.donation_type == type_edit.name:
            type_edit.quantity_total -= detail.quantity
            type_edit.save()
        form = DetailsDonationForm(request.POST, instance=detail)
        if form.is_valid():
            form.save()
            # Suma al total la cantidad editada
            if detail.donation_type == type_edit.name:
                type_edit.quantity_total += detail.quantity
                type_edit.save()
            return redirect('resume_donation', id=id_donator)
    else:
        form = DetailsDonationForm(instance=detail)
    return render(request, 'edit_donation.html', {'form': form})

# @login_required
# def delete_donation(request, id):
#     detail = get_object_or_404(DetailsDonation, pk=id)
#     id_donator = detail.donation_id
#     types = TypesDonation.objects.all()
#     type_res = TypesDonation.objects.get(name=detail.donation_type)
#     if request.method == 'POST':
#         if detail.donation_type == type_res.name:
#             type_res.quantity_total -= detail.quantity
#             type_res.save()
#         detail.delete()
#         delete_ok = True
#         return redirect('resume_donation', id=id_donator)
    # detail = get_object_or_404(DetailsDonation, pk=id)
    # id_donator = detail.donation_id
    # types = TypesDonation.objects.all()
    # type_res = TypesDonation.objects.get(name=detail.donation_type)
    # if detail.donation_type == type_res.name:
    #     type_res.quantity_total -= detail.quantity
    #     type_res.save()
    # detail.delete()
    # delete_ok = True
    # return redirect('resume_donation', id=id_donator)
@login_required
def delete_donation(request):
    # import ipdb; ipdb.set_trace()
    id = request.POST.get('donation_type_id')
    detail = DetailsDonation.objects.get(pk=id)
    types = TypesDonation.objects.all()
    type_res = TypesDonation.objects.get(name=detail.donation_type)
    if detail.donation_type == type_res.name:
        type_res.quantity_total -= detail.quantity
        type_res.save()
    response = {'type': detail.donation_type}
    detail.delete()
    return JsonResponse(response)

@login_required
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



@login_required
@staff_member_required(login_url='home')
def load_types_donation(request):

    if request.method == 'POST':
        form = LoadTypesDonationForm(request.POST)
        if form.is_valid():
            form.save()

    form = LoadTypesDonationForm()
    return render(request, 'load_types_donation.html', {'form': form})


@login_required
@staff_member_required(login_url='home')
def load_types_products(request):
    # TypesProducts.objects.filter(id=request.POST['id_type']).update(price=request.POST['price']) 
    types=TypesProducts.objects.all()
    
    context={'types':types}
    
    return render(request, 'load_types_product.html',context)

@login_required
@staff_member_required(login_url='home')
def update_price_article(request,id):
    article = TypesProducts.objects.get(pk=id)
    if request.method == "POST":
        form = LoadTypeProductForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('load_types_products')

    else:
        form = LoadTypeProductForm(instance=article)

    context={'form':form}
    return render(request,'upload_price_article.html',context)


@login_required
def sort_products(request):
    alert = False
    types_product=TypesProducts.objects.all()
    types = TypesDonation.objects.all()
    cargo=0
    if request.method == 'POST':
        form = SortProductForm(request.POST)
        if form.is_valid():
            sort=form.save(commit=False)
            cantidad = request.POST['quantity']
            tipo = request.POST['types']
            # guardo el tipo de producto
            x=TypesProducts.objects.get(id=tipo)

            # comparo 

            if x.name == 'Ropa Verano':
                d=TypesDonation.objects.get(name='Ropa')
                if Decimal(cantidad) > d.quantity_total:
                    
                    cargo=0
                    alert='El valor ingresado es mayor a la cantidad disponible'
                    ctotal=TypesProducts.objects.all()
                    control = TypesDonation.objects.filter(quantity_total__gt=0)
                    context = {'ctotal':ctotal,'control': control, 'form': form,'types_product':types_product,'alert':alert}
                    return render(request, 'sort_products.html', context)
                else:
                    cargo=1
                    sort.save()
            elif x.name == 'Ropa Invierno':
                d=TypesDonation.objects.get(name='Ropa')
                if Decimal(cantidad) > d.quantity_total:
                    cargo=0
                    alert='El valor ingresado es mayor a la cantidad disponible'
                    ctotal=TypesProducts.objects.all()
                    control = TypesDonation.objects.filter(quantity_total__gt=0)
                    context = {'ctotal':ctotal,'control': control, 'form': form,'types_product':types_product,'alert':alert}
                    return render(request, 'sort_products.html', context)
                else:
                    cargo=1
                    sort.save()
            elif TypesDonation.objects.filter(name=x.name).count() == 1:
                
                d=TypesDonation.objects.get(name=x.name)
                if Decimal(cantidad) > d.quantity_total:
                    
                    cargo=0
                    alert='El valor ingresado es mayor a la cantidad disponible'
                    context={'alert':alert}
                    ctotal=TypesProducts.objects.all()
                    control = TypesDonation.objects.filter(quantity_total__gt=0)
                    context = {'ctotal':ctotal,'control': control, 'form': form,'types_product':types_product,'alert':alert}
                    return render(request, 'sort_products.html', context)
                else:
                    cargo=1
                    sort.save()

           
            
            # agarro el ultimo agregado para sumar cantidad total 
            if cargo == 1:
                ultima_carga=SortProducts.objects.all().last()
                type_sum = TypesProducts.objects.get(name=ultima_carga.types)
                type_res = TypesProducts.objects.get(name=ultima_carga.types)
                if ultima_carga.types_id == type_sum.id:
                    type_sum.quantity_total += ultima_carga.quantity
                    type_sum.save()

                    if type_res.name == 'Ropa Verano':
                        bus=TypesDonation.objects.get(name='Ropa')
                        bus.quantity_total= bus.quantity_total - ultima_carga.quantity
                        bus.save()
                    elif type_res.name == 'Ropa Invierno':
                        bus=TypesDonation.objects.get(name='Ropa')
                        bus.quantity_total= bus.quantity_total - ultima_carga.quantity
                        bus.save()
                    elif TypesDonation.objects.filter(name=type_res.name).count() == 1 :
                        bus=TypesDonation.objects.get(name=type_res.name)
                        bus.quantity_total= bus.quantity_total - ultima_carga.quantity
                        bus.save()
            else:
                pass

        
            return redirect('sort_products')

    else:
        form = SortProductForm()

    art=TypesProducts.objects.all()
    control = TypesDonation.objects.filter(quantity_total__gt=0)
    control2 = TypesDonation.objects.filter(quantity_total__gt=0).exclude(name='Ropa')


    if TypesProducts.objects.count() != 0:
        for i in control:
            if i.name=='Ropa':
                if TypesProducts.objects.filter(name='Ropa Verano').count()==0:
                    p=TypesProducts()
                    p.name='Ropa Verano'
                    p.unit_measure=i.unit_measure
                    p.save()
                    p=TypesProducts()
                    p.name='Ropa Invierno'
                    p.unit_measure=i.unit_measure
                    p.save()
            else:
                if(TypesProducts.objects.filter(name=i.name).count()==0):
                    p=TypesProducts()
                    p.name=i.name
                    p.unit_measure=i.unit_measure
                    p.save()
    else:
        for i in control:
            if i.name == 'Ropa':
                p=TypesProducts()
                p.name='Ropa Verano'
                p.unit_measure=i.unit_measure
                p.save()
                p=TypesProducts()
                p.name='Ropa Invierno'
                p.unit_measure=i.unit_measure
                p.save()
            else:
                p=TypesProducts()
                p.name=i.name
                p.unit_measure=i.unit_measure
                p.save()

    ctotal=TypesProducts.objects.all()

    context = {'ctotal':ctotal,'control': control, 'form': form,'types_product':types_product,'alert':alert}
    return render(request, 'sort_products.html', context)

@login_required
def fix_products(request):
    alert = False
    types_product=TypesFix.objects.all()
    types = TypesDonation.objects.all()
    cargo=0
    if request.method == 'POST':
        form = FixProductForm(request.POST)
        if form.is_valid():
            sort=form.save(commit=False)
            cantidad = request.POST['quantity']
            tipo = request.POST['types']
            # guardo el tipo de producto
            x=TypesFix.objects.get(id=tipo)

            # comparo 
            if TypesDonation.objects.filter(name=x.name).count() == 1:
                d=TypesDonation.objects.get(name=x.name)
                if Decimal(cantidad) > d.quantity_total:
                    cargo=0
                    alert='El valor ingresado es mayor a la cantidad disponible'
                    context={'alert':alert}
                    ctotal=TypesFix.objects.all()
                    control = TypesDonation.objects.filter(quantity_total__gt=0)
                    context = {'ctotal':ctotal,'control': control, 'form': form,'types_product':types_product,'alert':alert}
                    return render(request, 'fix_products.html', context)
                else:
                    cargo=1
                    sort.save()
            # agarro el ultimo agregado para sumar cantidad total 
            if cargo == 1:
                ultima_carga=FixProducts.objects.all().last()
                type_sum = TypesFix.objects.get(name=ultima_carga.types)
                type_res = TypesFix.objects.get(name=ultima_carga.types)
                if ultima_carga.types_id == type_sum.id:
                    type_sum.quantity_total += ultima_carga.quantity
                    type_sum.save()

                    if TypesDonation.objects.filter(name=type_res.name).count() == 1 :
                        bus=TypesDonation.objects.get(name=type_res.name)
                        bus.quantity_total= bus.quantity_total - ultima_carga.quantity
                        bus.save()
            else:
                pass
            return redirect('fix_products')
    else:
        form = FixProductForm()

    control = TypesDonation.objects.filter(quantity_total__gt=0)
    if TypesFix.objects.count() != 0:
        for i in control:
            if(TypesFix.objects.filter(name=i.name).count()==0):
                p=TypesFix()
                p.name=i.name
                p.unit_measure=i.unit_measure
                p.save()
    else:
        for i in control:
            p=TypesFix()
            p.name=i.name
            p.unit_measure=i.unit_measure
            p.save()

    ctotal=TypesFix.objects.all()

    context = {'ctotal':ctotal,'control': control, 'form': form,'types_product':types_product,'alert':alert}
    return render(request, 'fix_products.html', context)
    

@login_required
def carry_out(request,id):
    alert = False
    responsable = ResponsableFix.objects.get(pk=id)
    types=TypesFix.objects.filter(quantity_total__gt=0)
    carry = Carry.objects.filter(responsable__pk=responsable.id)
    if request.method == 'POST':
        form_carry = CarryForm(request.POST)
        if form_carry.is_valid():
            load = form_carry.save(commit=False)
            load.types = request.POST['types']
            load.unit_measure = request.POST['unit_measure']
            load.responsable_id = responsable.id
            # load.save()

            type_res = TypesFix.objects.get(name=load.types)
            if load.types == type_res.name:
                if load.quantity > type_res.quantity_total:
                    cargo=0
                    alert='El valor ingresado es mayor a la cantidad disponible'
                    context={'types':types,'responsable':responsable,'form_carry':form_carry,'alert':alert}
                    return render(request, 'carry_out.html', context)
                else:
                    cargo=1
                    load.save()
                    type_res.quantity_total -= load.quantity
                    type_res.save()
            return redirect('carry_out', id=id)
    else:
        form_carry = CarryForm()

    context={'types':types,'responsable':responsable,'form_carry':form_carry,'alert':alert}

    return render(request,'carry_out.html',context)

@login_required
def responsable(request):
    form = ResponsableForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            responsable = ResponsableFix.objects.last()
            return redirect('carry_out',id=responsable.id)
    context = {'form': form}
    return render(request, 'responsable.html', context)

def resume_fix(request, id):
    responsable = ResponsableFix.objects.get(pk=id)
    q1=Q(responsable__pk=id)
    q2=Q(quantity__gt=0)
    resumes = Carry.objects.filter(q1&q2)
    if request.method == "POST":
        fix_form = CarryForm(request.POST, instance=responsable)
        if fix_form.is_valid():
            fix_form.save()
            return redirect('resume_fix', id=responsables.id)
    else:
        fix_form = DonationForm(instance=responsable)
    context = {'responsable': responsable, 'resumes': resumes, 'don_form': fix_form}
    return render(request, 'resume_fix.html', context)

def delete_fix(request, id):
    carry = get_object_or_404(Carry, pk=id)
    id_responsable = carry.responsable_id
    types = TypesFix.objects.all()
    type_res = TypesFix.objects.get(name=carry.types)
    if carry.types == type_res.name:
        type_res.quantity_total += carry.quantity
        type_res.save()
    carry.delete()
    return redirect('resume_fix', id=id_responsable)
    
@login_required
def list_sort(request):
    list_donations=TypesDonation.objects.filter(quantity_total__gt=0)

    context={'list_donations':list_donations}
    return render(request,'list_sort.html',context)

def list_fix(request):
    resp=ResponsableFix.objects.all()
    carry=Carry.objects.filter(quantity__gt=0)
    list_res=[]
    for r in resp:
        q1=Q(responsable_id=r.id)
        q2=Q(quantity__gt=0)
        if Carry.objects.filter(q1 & q2).count() > 0:
            list_res.append(r)
            r.state = 0
            r.save()

    print(list_res,'Cantidad de responsables')
    context={'resp':list_res,'carry':carry}
    return render(request,'list_fix.html',context)

def give_back(request,id):
    carry = get_object_or_404(Carry, pk=id)
    
    id_resp = carry.responsable_id
    responsable=ResponsableFix.objects.get(id=id_resp)
    types = TypesDonation.objects.all()
    # others = Carry.objects.filter(responsable=id_resp)
    
    type_edit = types.get(name=carry.types)
    if carry.types == type_edit.name:
        type_edit.quantity_total += carry.quantity
        type_edit.save()
        carry.quantity_back+=carry.quantity
        carry.quantity=0
        carry.save()


    q1=Q(responsable=id_resp)
    q2=Q(quantity__gt=0)

    if Carry.objects.filter(q1 & q2).count() > 0:
        print('todavia falta devolver')
        responsable.state = 0
        responsable.save()
    else:
        print('Ya devolvio todo')
        responsable.state = 1
        responsable.save()
        
    return redirect('list_fix')

def agregate_responsable(request):
    resp=ResponsableFix.objects.all()
    carry=Carry.objects.filter(quantity__gt=0)

    context={'resp':resp}
    return render(request,'agregate_responsable.html',context)


@login_required
def register_referring(request):
    form_refering = ReferringForm(request.POST or None)
    form_family = FamilyForm_r(request.POST or None)

    neigh = Neighborhood.objects.all()
    if request.method == 'POST':
        if form_refering.is_valid() and form_family.is_valid() :
            fam = form_family.save(commit=False)
            fam.role = 'r'
            fam.birth = request.POST['birth']
            fam.save()

            family = Family.objects.get(id=fam.id)

            family.ref = fam.id
            family.save()
            
            ref = form_refering.save(commit=False)
            ref.family = family
            ref.neighborhood_id = request.POST['neigh_id']
            ref.save()
            return redirect('/referente/'+str(ref.id)+'/')

    form = {'form_refering':form_refering,'form_family':form_family,'neigh':neigh}
    template = 'register_referring.html'

    return render(request, template, form)

@login_required
def register_family(request, id):
    form = FamilyForm(request.POST or None)
    ref = Referring.objects.get(pk=id)
    if request.method == 'POST':
        if form.is_valid():
            fam = form.save(commit=False)
            fam.ref = ref.family_id
            fam.role = 'f'
            fam.birth = request.POST['birth']
            fam.save()
            fam_id=fam.id
            return redirect('/referente/familiares/perfil_familiar/'+str(fam_id)+'/')
    return render(request, 'register_family.html', {'form': form})


@login_required
def referring_search(request):
    ref = Family.objects.filter(role__exact='r')
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            q1 = Q(firstname__contains=query)
            q2 = Q(lastname__contains=query)
            q3 = Q(dni__exact=query)
            if query.isdigit():
                ref = Family.objects.filter(q3)
                total = Family.objects.filter(q3).count()
            else:
                ref = Family.objects.filter(q1 | q2)
                total = Family.objects.filter(q1 | q2).count()                
            return render(request, 'referring_search_out.html', {'ref': ref,
                                                                 'query': query,
                                                                 'total': total})
    else:
        form = SearchForm()
    return render(request, 'referring_search.html', {'form': form,
                                                     'ref': ref})


@login_required
def referring_profile(request, id):
    ref = Referring.objects.get(pk=id)
    return render(request, 'referring_profile.html', {'ref': ref})


@login_required
def referring_relatives(request, id):
    ref = Referring.objects.get(pk=id)
    fam = Family.objects.filter(ref=ref.family.id)
    return render(request, 'referring_relatives.html', {'ref': ref,
                                                        'fam': fam})

@login_required
def relative_profile(request,id):
    # import ipdb; ipdb.set_trace()
    fam = Family.objects.get(pk=id)
    ref = Referring.objects.get(family_id=fam.ref)
    return render(request, 'relative_profile.html', {'fam': fam,
                                                    'ref': ref})

@login_required
def edit_referring(request,id):
    ref = Referring.objects.get(pk=id)
    family = Family.objects.get(id=ref.family_id)
    neigh = Neighborhood.objects.all()
    if request.method == 'POST':
        form1 = FamilyForm_r(request.POST, instance=family)
        if form1.is_valid():
            fam1 = form1.save(commit=False)
            fam1.birth = request.POST['birth']
            fam1.save()
        form2 = ReferringForm(request.POST, instance=ref)
        if form2.is_valid():
            fam = form2.cleaned_data
            fam = form2.save(commit=False)
            fam.family = family
            fam.neighborhood_id = request.POST['neigh_id']
            fam.save()
        if form1.is_valid() and form2.is_valid():
            return redirect('referring_profile', id)
    else:
        form1 = FamilyForm_r(instance=family)
        form2 = ReferringForm(instance=ref)
    return render(request,'edit_referring.html',{'form1':form1,
                                                 'form2':form2,
                                                 'neigh': neigh,
                                                 'ref':ref})

@login_required
def edit_family(request,id):
    family = Family.objects.get(pk=id)
    if request.method == 'POST':
        form = FamilyForm(request.POST, instance=family)
        if form.is_valid():
            fam = form.save(commit=False)
            fam.birth = request.POST['birth']
            fam.save()
        return redirect('relative_profile', id)
    else:
        form = FamilyForm(instance=family)
    return render(request,'edit_family.html',{'form':form, 'family':family})

@login_required
@staff_member_required(login_url='home')
def neigh(request):
    neigh = Neighborhood.objects.all()
    if request.method == 'POST':
        form = NeighForm(request.POST)
        if form.is_valid():
            form.save()
    form = NeighForm()
    return render(request, 'neigh.html', {'form': form,
                                          'neigh': neigh})

@login_required
@staff_member_required(login_url='home')
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

@login_required
@staff_member_required(login_url='home')
def del_neigh(request, id):
    neigh = get_object_or_404(Neighborhood, pk=id)
    neigh.delete()
    return redirect('neigh')


def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = LoginForm(request.POST or None)
    if request.POST and form.is_valid():
        #import ipdb; ipdb.set_trace()
        user = form.login(request)
        if user is not None:
            log(request, user)
            request.session['member_id'] = user.id
            request.session.set_expiry(14400) #86400 = 24hs     # 3600 = 1hr
            return redirect('home')# Redirect to a success page.
    return render(request,'login.html',{'form': form})
    # if request.method == "POST":
    #     username = request.POST['username']
    #     password = request.POST['password']
    #     username = username.upper()
    #     user = authenticate(request,username=username,password=password)
    #     if user is not None:
    #         log(request,user)
    #         request.session['member_id'] = user.id
    #         request.session.set_expiry(14400) #86400 = 24hs     # 3600 = 1hr

    #         return redirect('home')
    # form = LoginForm()
    # return render(request,'login.html',{'form': form})

@login_required
def logout(request):
    logout_django(request)
    return redirect('login')

@login_required
def closet(request):
    fam = Family.objects.all()
    ref = Referring.objects.all()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            # import ipdb; ipdb.set_trace()
            query = form.cleaned_data['query']
            q1 = Q(firstname__contains=query)
            q2 = Q(lastname__contains=query)
            q3 = Q(dni__exact=query)
            if query.isdigit():
                fam = Family.objects.filter(q3)
            else:
                fam = Family.objects.filter(q1 or q2)
            return render(request, 'closet_search_out.html', {'fam': fam,
                                                              'query': query})
    else:
        form = SearchForm()
    return render(request,'entry_closet.html',{'form':form,
                                         'fam':fam})

@login_required
def entry_ok(request,id):
    fam = Family.objects.get(pk=id)
    ref = Referring.objects.get(family_id = fam.ref)
    today_month = datetime.date.today().month
    today = datetime.date.today()
    all_entry = FamilyEntry.objects.all()
    while True:
        try:
            entry = FamilyEntry.objects.get(family_id=ref.id,last_entry__month=today.month)
            break
        except FamilyEntry.DoesNotExist:
            entry = None
            break

    # import ipdb; ipdb.set_trace()
    if fam.role == 'r':
        last_buy = fam.referring.last_buy
    else:
        last_buy = ref.last_buy

    if entry == None:
        if last_buy:
            last_buy_date = last_buy.month
            if ((today_month)-(last_buy_date) > 0):
                fam_e = FamilyEntry()
                fam_e.family = fam
                fam_e.save()
                return render(request,'entry_ok.html',{'fam':fam})
            else:
                return render(request,'entry_fail.html',{'fam':fam})
        else:
            fam_e = FamilyEntry()
            fam_e.family = fam
            fam_e.save()
            return render(request,'entry_ok.html',{'fam':fam})
    else:
        return render(request,'entry_fail.html',{'fam':fam})

@login_required
@staff_member_required(login_url='home')
def register_user(request):
    if request.method == 'POST':
        form_user = UserRegisterForm(request.POST)
        form_profile = ProfileForm(request.POST)
        if form_user.is_valid() and form_profile.is_valid():
            form_user.save()
            user = form_user.save(commit=False)
            form_profile = ProfileForm(request.POST, instance=user.profile)
            if form_profile.is_valid():
                prof = form_profile.save(commit=False)
                prof.phone_number = request.POST["phone_number"]
                prof.save()
                username = form_user.cleaned_data.get('username')
                messages.success(request, f'La cuenta fue creada, ahora {username} puede iniciar sesion')
                return redirect('home')
    else:
        form_user = UserRegisterForm()
        form_profile = ProfileForm()
    return render(request, 'register_user.html', {'form_user': form_user, 'form_profile': form_profile})

@login_required
def peoples_closet(request):
    today = datetime_django.today()
    peoples = FamilyEntry.objects.filter(last_entry__year=today.year, last_entry__month=today.month, last_entry__day=today.day)
    ref = Referring.objects.all()
    id_excludes = []
    for p in peoples:
        # import ipdb; ipdb.set_trace()
        if p.family.role == 'r':
            referente = Referring.objects.get(family_id=p.family_id)
            if referente.last_buy != None:
                if referente.last_buy.year==today.year and referente.last_buy.month==today.month and referente.last_buy.day==today.day:
                    #peoples.exclude(family_id=p.family_id)
                    id_excludes.append(p.family_id)
        else:
            referente = Referring.objects.get(family_id=p.family.ref)
            if referente.last_buy != None:
                if referente.last_buy.year==today.year and referente.last_buy.month==today.month and referente.last_buy.day==today.day:
                    #peoples.exclude(family_id=p.family_id)
                    id_excludes.append(p.family_id)

    peoples = peoples.exclude(family_id__in=id_excludes)
    context = {'peoples':peoples, 'ref': ref, 'today':today}
    return render(request, 'peoples_closet.html', context)

@login_required
def exit_closet(request, id):
    entry = FamilyEntry.objects.get(pk=id)
    entry.delete()
    return redirect('peoples_closet')

@login_required
def sale(request, id):
    #import ipdb; ipdb.set_trace()
    try:
        ventas = Sale.objects.get(entry_id = id)
    except  Sale.DoesNotExist :
        ventas = None

    if ventas is None:
        entry = FamilyEntry.objects.get(pk=id)
        sale = Sale(total=0, entry_id=id)
        sale.save()
        return redirect('sale_detail', id)
    else:
        return redirect('sale_detail', id)

@login_required
def sale_detail(request,id):
    # import ipdb; ipdb.set_trace()
    alert = False
    entry = FamilyEntry.objects.get(pk=id)
    types = TypesProducts.objects.all()
    sale = Sale.objects.get(entry_id = id)
    sale_details = SalesDetails.objects.filter(sale_id=sale.id)
    if request.method == 'POST':
        form = SalesDetailsForm(request.POST)
        if form.is_valid():
            # import ipdb; ipdb.set_trace()
            detail = form.save(commit=False)
            detail.product_type = request.POST['product_type']
            detail.unit_measure = request.POST['unit_measure']
            detail.price = request.POST['price']
            # Para cantidad en kg con num despues de la coma
            if (Decimal(detail.quantity) % 1 == 0):
                detail.total = int(detail.price) * int(detail.quantity)
            else:
                 detail.total = float(detail.price) * float(detail.quantity)
            
            detail.sale_id = sale.id
            detail.save()

            # Restar la cantidad vendida de product_types
            type_res = TypesProducts.objects.get(name=detail.product_type)
            if detail.product_type == type_res.name:
                # Control producto ropa 1.5kg por cada venta
                if detail.product_type == 'Ropa Invierno' or detail.product_type == 'Ropa Verano':
                    if detail.quantity > 1.5:
                        alert = 'Solo se permite 1.5Kg por cada venta'
                        detail.delete()
                        form = SalesDetailsForm()
                        context = {'entry': entry, 'types': types, 'form': form, 
                                    'sale': sale, 'sale_details': sale_details, 'alert': alert}
                        return render(request, 'sales.html', context)
                # Control producto calzado 2 pares por cada venta
                if detail.product_type == 'Calzados':
                    if detail.quantity > 2:
                        alert = 'Solo se permite 2 pares por cada venta'
                        detail.delete()
                        form = SalesDetailsForm()
                        context = {'entry': entry, 'types': types, 'form': form, 
                                    'sale': sale, 'sale_details': sale_details, 'alert': alert}
                        return render(request, 'sales.html', context)   
                if type_res.quantity_total < detail.quantity:
                    alert = 'La cantidad ingresada es mayor a la disponible en el ropero'
                    detail.delete()
                    form = SalesDetailsForm()
                    context = {'entry': entry, 'types': types, 'form': form, 
                                'sale': sale, 'sale_details': sale_details, 'alert': alert}
                    return render(request, 'sales.html', context)
                else:
                    type_res.quantity_total -= detail.quantity
                    type_res.save()
                    sale.total += detail.total
                    sale.save()
                    return redirect('sale_detail', id)
    else:
        form = SalesDetailsForm()
    context = {'entry': entry, 'types': types, 'form': form, 
                'sale': sale, 'sale_details': sale_details, 'alert': alert}
    return render(request, 'sales.html', context)

@login_required
def summary_sale(request, id):
    sale = Sale.objects.get(entry_id=id)
    details = SalesDetails.objects.filter(sale_id=sale.id)
    entry = FamilyEntry.objects.get(pk=id)
    if entry.family.role == 'r':
        ref = Referring.objects.get(family_id=entry.family_id)
    else:
        ref = Referring.objects.get(family_id=entry.family.ref)

    if request.method == 'POST':
        form = TotalForm(request.POST, instance=sale)
        if form.is_valid():
            form.save()
            ref.last_buy = entry.last_entry
            ref.family_last_buy = entry.family.lastname+", "+entry.family.firstname
            ref.save()
            return redirect('peoples_closet')
    else:
        form = TotalForm(instance=sale)
    context = {'sale': sale, 'details': details, 'entry': entry, 'form': form}
    return render(request, 'summary_sale.html', context)
  
@login_required
def delete_sale(request):
    # import ipdb; ipdb.set_trace()
    id = request.POST.get('sale_type_id')
    detail = SalesDetails.objects.get(pk=id)
    sale = Sale.objects.get(pk=detail.sale_id)
    sale.total -= detail.total
    sale.save()

    type_sum = TypesProducts.objects.get(name=detail.product_type)
    if detail.product_type == type_sum.name:
        type_sum.quantity_total += detail.quantity
        type_sum.save()
    response = {'type_id': detail.id}
    detail.delete()
    return JsonResponse(response)

@login_required
# @staff_member_required(login_url='home')
def home(request):
    today = datetime.date.today()  
    #Datos ventas
    data_s = SalesDetails.objects.filter(sale__entry__last_entry__month=today.month).values('product_type').annotate(total=Sum('quantity'))
    #Datos donaciones
    data_d = DetailsDonation.objects.filter(donation__date__month=today.month).values('donation_type').annotate(total=Sum('quantity'))
    # Precios
    # prices = SalesDetails.objects.filter(sale__entry__last_entry__year=today.year,sale__entry__last_entry__month=today.month,sale__entry__last_entry__day=today.day).values('product_type').annotate(total=Sum('price'))
    #Usuarios
    users = User.objects.filter(is_superuser=0)
    #Lista de articulos
    arts = TypesProducts.objects.all()

    donations = TypesDonation.objects.all()

    # import ipdb; ipdb.set_trace()
    return render(request,'home.html',{# Donaciones
                                           'data_d':data_d,
                                           #Ventas
                                           'data_s':data_s,

                                           'users':users,
                                           'arts':arts,
                                           'donations':donations})

@login_required
def profile_user(request):
    user = request.user

    return render(request, 'profile_user.html', {'user': user})

@login_required
def credits(request):
    return render(request,'credits.html',{})

@login_required
def profile_user_edit(request, id):
    user = User.objects.get(pk=id)
    profile = Profile.objects.get(user_id=id)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        form_profile = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid() and form_profile.is_valid():
            form.save()
            form_profile.save()
            return redirect('profile_user')
    else:
        form = UserRegisterForm(instance=user)
        form_profile = ProfileUpdateForm(instance=profile)
    context = {'form': form, 'form_profile':form_profile}
    return render(request, 'profile_user_edit.html', context)


@login_required
def change_password(request, id):
    user = User.objects.get(pk=id)
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('profile_user')
        
    else:
        form = PasswordChangeForm(user)
    return render(request, 'change_password.html', {'form': form})

@login_required
@staff_member_required(login_url='home')
def sales_report(request):

    today = datetime_django.today()
    types = TypesProducts.objects.all()

    data = SalesDetails.objects.filter(sale__entry__last_entry__month=today.month).values('product_type').annotate(total=Sum('quantity'))

    if request.method == 'POST':
        # import ipdb; ipdb.set_trace()

        begin = request.POST['begin']
        begin = datetime.datetime.strptime(begin,"%Y-%m-%d").date()
        finish = request.POST['finish']
        finish = datetime.datetime.strptime(finish,"%Y-%m-%d").date()
        sale = request.POST.getlist('sale_id')
        q1 = Q(sale__entry__last_entry__gte=begin)
        q2 = Q(sale__entry__last_entry__lte=finish)
        q3 = Q(product_type__in=sale)

        # Reporte de ventas con tipo de prod, fecha inicio y fecha final
        report = list(SalesDetails.objects.filter(q3 & q1 & q2).values('product_type',
                                                                        'unit_measure',
                                                                        'total',
                                                                        'quantity',
                                                                        'sale__entry__last_entry',
                                                                        'sale__entry__family__firstname',
                                                                        'sale__entry__family__lastname',))
        
        # Reporte 2 con total por producto
        report2 = list(SalesDetails.objects.filter(q3 & q1 & q2).values('unit_measure',product_type_total=F('product_type')).annotate(product_total=Sum('quantity')))

        # Cambio en report cantidad en decimal por float
        for i in range(0,len(report)):
            report[i]['quantity'] = float(report[i]['quantity'])

        for i in range(0,len(report2)):
            report2[i]['product_total'] = float(report2[i]['product_total'])


        report = report + report2
        return JsonResponse(report, safe=False)

    return render(request, 'sales_report.html', {'data':data, 'types': types})


# @login_required
# @staff_member_required(login_url='home')
# def donations_report(request):
#     dona = TypesDonation.objects.all()
#     today = datetime.date.today()
#     if request.method == 'POST':

#         begin = request.POST['begin']
#         finish = request.POST['finish']
#         donation = request.POST['dona_id']

#         if begin == '':
#             begin = today
#         else:
#             begin = datetime.datetime.strptime(begin,"%Y-%m-%d").date()
#         if finish == '':
#             finish = today
#         else:
#             finish = datetime.datetime.strptime(finish,"%Y-%m-%d").date()


#         import ipdb; ipdb.set_trace()

#         q1 = Q(donation__date__gte=begin)
#         q2 = Q(donation__date__lte=finish)
#         q3 = Q(donation_type__exact=donation)
#         report = DetailsDonation.objects.filter(q3 & q1 & q2).values('donation_type').annotate(total=Sum('quantity'))
#         all_reports = DetailsDonation.objects.filter(q3 & q1 & q2)

#         return render(request,'donations_report_result.html',{'report':report,
#                                                               'don':donation,
#                                                               'begin': begin,
#                                                               'finish':finish,
#                                                               'all':all_reports})

#     else:
#         form = DonationsReportForm()
#     return render(request,'donations_report.html',{'form':form,
#                                                    'dona':dona})

@login_required
@staff_member_required(login_url='home')
def donations_report(request):

    today = datetime_django.today()
    types = TypesDonation.objects.all()

    data = DetailsDonation.objects.filter(donation__date__month=today.month).values('donation_type').annotate(total=Sum('quantity'))

    if request.method == 'POST':
        # import ipdb; ipdb.set_trace()

        begin = request.POST['begin']
        begin = datetime.datetime.strptime(begin,"%Y-%m-%d").date()
        finish = request.POST['finish']
        finish = datetime.datetime.strptime(finish,"%Y-%m-%d").date()
        donation = request.POST.getlist('dona_id')
        q1 = Q(donation__date__gte=begin)
        q2 = Q(donation__date__lte=finish)
        q3 = Q(donation_type__in=donation)

        # Reporte de ventas con tipo de prod, fecha inicio y fecha final
        report = list(DetailsDonation.objects.filter(q3 & q1 & q2).values('donation_type',
                                                                        'unit_measure',
                                                                        'quantity',
                                                                        'donation__date',
                                                                        'donation__name',))
        
        # Reporte 2 con total por producto
        # report2 = list(SalesDetails.objects.filter(q3 & q1 & q2).values(product_type_total=F('product_type')).annotate(product_total=Sum('quantity')))

        # Cambio en report cantidad en decimal por float
        for i in range(0,len(report)):
            report[i]['quantity'] = float(report[i]['quantity'])

        # for i in range(0,len(report2)):
        #     report2[i]['product_total'] = float(report2[i]['product_total'])

        return JsonResponse(report, safe=False)

    return render(request, 'donations_report.html', {'data':data, 'types': types})