from django.core.validators import MaxValueValidator
from django.db import models

# Create your models here.
UNITS_MEASURE = (('kg', 'Kg'), ('par', 'Par'), ('un', 'Unidad'), ('lt', 'Litro'))


class Donation(models.Model):
    date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=80)
    ticket_number = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class DetailsDonation(models.Model):
    donation_type = models.CharField(max_length=30)
    unit_measure = models.CharField(max_length=10, choices=UNITS_MEASURE)
    quantity = models.IntegerField()
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name='detailsdonation')


class TypesDonation(models.Model):
    name = models.CharField(max_length=30)
    unit_measure = models.CharField(max_length=10, choices=UNITS_MEASURE)
    quantity_total = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Neighborhood(models.Model):
    name = models.CharField(max_length=30)


class Family(models.Model):
	lastname = models.CharField(max_length=30)
	firstname = models.CharField(max_length=30)
	dni = models.PositiveIntegerField()#Limitar numeros
	birth = models.DateField(null=True)
	role = models.CharField(max_length=1,choices=(('r','Referente'),('f','Familiar')))

class Referring(models.Model):
	neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, related_name='referentes', null=True)
	phone = models.PositiveIntegerField()#Limitar numero de telefono
	adress = models.CharField(max_length=80)
	family = models.OneToOneField(Family, on_delete=models.CASCADE)
	last_buy = models.DateTimeField(null=True)
	family_last_buy = models.CharField(max_length=65,null=True)
