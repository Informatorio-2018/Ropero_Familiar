from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.db.models import Q, Sum
from django.contrib.auth import authenticate, login as log, logout as logout_django
from django.contrib.auth.decorators import login_required
from django.utils.timezone import datetime as datetime_django
import datetime
from decimal import Decimal

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

@login_required
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

@login_required
def donations_report(request):
    dona = TypesDonation.objects.all()
    today = datetime.date.today()
    if request.method == 'POST':
        begin = request.POST['begin']
        finish = request.POST['finish']
        donation = request.POST['dona_id']
        if begin == '':
            begin = today
        else:
            begin = datetime.datetime.strptime(begin,"%Y-%m-%d").date()
        if finish == '':
            finish = today
        else:
            finish = datetime.datetime.strptime(finish,"%Y-%m-%d").date()
        q1 = Q(donation__date__year__gte=begin.year,donation__date__month__gte=begin.month,donation__date__day__gte=begin.day)
        q2 = Q(donation__date__year__lte=finish.year,donation__date__month__lte=finish.month,donation__date__day__lte=finish.day)
        q3 = Q(donation_type__exact=donation)
        report = DetailsDonation.objects.filter(q3 & q1 & q2).aggregate(total=Sum('quantity'))
        all_reports = DetailsDonation.objects.filter(q3 & q1 & q2)
        return render(request,'donations_report_result.html',{'report':report['total'],
                                                              'don':donation,'don1':all_reports[0], 'begin': begin, 'finish':finish,
                                                              'all':all_reports})
    else:
        form = DonationsReportForm()
    return render(request,'donations_report.html',{'form':form,
                                                   'dona':dona})

@login_required
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


@login_required
def load_types_donation(request):

    if request.method == 'POST':
        form = LoadTypesDonationForm(request.POST)
        if form.is_valid():
            form.save()

    form = LoadTypesDonationForm()
    return render(request, 'load_types_donation.html', {'form': form})


@login_required
def load_types_products(request):
    # TypesProducts.objects.filter(id=request.POST['id_type']).update(price=request.POST['price']) 
    types=TypesProducts.objects.all()
    
    context={'types':types}
    
    return render(request, 'load_types_product.html',context)

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
                    return render(request, 'sort_products.html', context)
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
    
    # return render(request,'fix_products.html')


def carry_out(request,id):
    responsable = ResponsableFix.objects.get(pk=id)
    types=TypesFix.objects.all()
    carry = Carry.objects.filter(responsable__pk=responsable.id)
    if request.method == 'POST':
        form_carry = CarryForm(request.POST)
        if form_carry.is_valid():
            load = form_carry.save(commit=False)
            load.types = request.POST['types']
            load.unit_measure = request.POST['unit_measure']
            load.responsable_id = responsable.id
            load.save()

            type_res = TypesFix.objects.get(name=load.types)
            if load.types == type_res.name:
                type_res.quantity_total -= load.quantity
                type_res.save()
            return redirect('carry_out', id=id)
    else:
        form_carry = CarryForm()


    context={'types':types,'responsable':responsable,'form_carry':form_carry}

    return render(request,'carry_out.html',context)

def responsable(request):
    form = ResponsableForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            responsable = ResponsableFix.objects.last()
            return redirect('carry_out',id=responsable.id)
    context = {'form': form}
    return render(request, 'responsable.html', context)
    


@login_required
def register_family(request, id):
    form = FamilyForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            fam = form.save(commit=False)
            fam.ref = id
            fam.role = 'f'
            fam.birth = request.POST['birth']
            fam.save()
            return redirect('/referente/'+str(id)+'/familiares/')
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
            q3 = Q(role__exact='r')
            ref = Family.objects.filter((q1 & q3) | (q2 & q3))
            total = Family.objects.filter((q1 & q3) | (q2 & q3)).count()
            return render(request, 'referring_search_out.html', {'ref': ref,
                                                                 'query': query,
                                                                 'total': total})
    else:
        form = SearchForm()
    return render(request, 'referring_search.html', {'form': form,
                                                     'ref': ref})


@login_required
def referring_profile(request, id):
    ref = Family.objects.get(pk=id)
    return render(request, 'referring_profile.html', {'ref': ref})


@login_required
def referring_relatives(request, id):
    ref = Family.objects.get(pk=id)
    fam = Family.objects.filter(ref=id)
    return render(request, 'referring_relatives.html', {'ref': ref,
                                                        'fam': fam})

@login_required
def relative_profile(request,id):
    fam = Family.objects.get(pk=id)
    return render(request, 'relative_profile.html', {'fam': fam})


#@login_required
def home(request):
    return render(request, 'home.html', {})

@login_required
def edit_referring(request,id):
    family = Family.objects.get(pk=id)
    neigh = Neighborhood.objects.all()
    ref = Referring.objects.get(family_id=id)
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

@login_required
def closet(request):
    fam = Family.objects.all()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            q1 = Q(firstname__contains=query)
            q2 = Q(lastname__contains=query)
            fam = Family.objects.filter(q1 | q2)
            return render(request, 'closet_search_out.html', {'fam': fam,
                                                              'query': query})
    else:
        form = SearchForm()
    return render(request,'entry_closet.html',{'form':form,
                                         'fam':fam})

@login_required
def entry_ok(request,id):
    fam = Family.objects.get(pk=id)
    today_month = datetime.date.today().month

    if fam.role == 'r':
        last_buy = fam.referring.last_buy
    else:
        ref = Referring.objects.get(family_id=fam.ref)
        last_buy = ref.last_buy

    if last_buy:
        last_buy_date = last_buy.month
        if (today_month)-(last_buy_date) > 0:
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

@login_required
def register_user(request):
    if request.method == 'POST':
        # import ipdb; ipdb.set_trace()
        form_user = UserRegisterForm(request.POST)
        if form_user.is_valid():
            user = form_user.save(commit=False)
            user.save()
            profile = Profile()
            profile.user_id = user.id
            profile.phone_number = request.POST['phone_number']
            profile.save()
            return redirect('home')
    else:
        form_user = UserRegisterForm()
    return render(request, 'register_user.html', {'form_user': form_user})

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
    entry = FamilyEntry.objects.get(pk=id)
    types = TypesProducts.objects.all()
    sale = Sale.objects.get(entry_id = id)
    sale_details = SalesDetails.objects.filter(sale_id=sale.id)
    if request.method == 'POST':
        form = SalesDetailsForm(request.POST)
        if form.is_valid():
            detail = form.save(commit=False)
            detail.product_type = request.POST['product_type']
            detail.unit_measure = request.POST['unit_measure']
            detail.price = request.POST['price'] 
            detail.total = int(detail.price) * int(detail.quantity)
            detail.sale_id = sale.id
            sale.total += detail.total
            sale.save()
            detail.save()
            return redirect('sale_detail', id)
    else:
        form = SalesDetailsForm()
    context = {'entry': entry, 'types': types, 'form': form, 
                'sale': sale, 'sale_details': sale_details}
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
def delete_sale(request, id):
    detail = get_object_or_404(SalesDetails, pk=id)
    sale = Sale.objects.get(pk=detail.sale_id)
    sale.total -= detail.total
    sale.save()
    detail.delete()
    return redirect('summary_sale', id=sale.entry_id)