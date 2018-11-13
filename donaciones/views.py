from django.shortcuts import render, redirect
from .forms import FamilyForm, DonationForm

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
