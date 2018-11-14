from django.core.validators import MaxValueValidator
from django.db import models

# Create your models here.


class Donation(models.Model):
    date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=80)
    clothes = models.DecimalField(max_digits=4, decimal_places=3)
    shoes = models.PositiveIntegerField(validators=[MaxValueValidator(4)])
    accesories = models.PositiveIntegerField(validators=[MaxValueValidator(4)])
    ticket_number = models.PositiveIntegerField(validators=[MaxValueValidator(8)])

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