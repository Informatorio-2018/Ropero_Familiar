from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.
UNITS_MEASURE = (('kg', 'Kg'), ('par', 'Par'), ('un', 'Unidad'), ('lt', 'Litro'))


class Donation(models.Model):
    date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=80, verbose_name='Nombre o Razón Social')
    ticket_number = models.IntegerField(null=True, verbose_name='Numero de Recibo')

    def __str__(self):
        return self.name


class DetailsDonation(models.Model):
    donation_type = models.CharField(max_length=30, verbose_name='Tipo de Donación')
    unit_measure = models.CharField(max_length=10, choices=UNITS_MEASURE, verbose_name='Unidad de Medida')
    quantity = models.IntegerField(verbose_name='Cantidad')
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name='detailsdonation')

    def __str__(self):
        return self.donation_type


class TypesDonation(models.Model):
    name = models.CharField(max_length=30, verbose_name='Nombre')
    unit_measure = models.CharField(max_length=10, choices=UNITS_MEASURE, verbose_name='Unidad de Medida')
    quantity_total = models.IntegerField(default=0, verbose_name='Cantidad Total')

    def __str__(self):
        return self.name


class Neighborhood(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return "%s" % (self.name)

class Family(models.Model):
    lastname = models.CharField(max_length=30,verbose_name='Nombre')
    firstname = models.CharField(max_length=30,verbose_name='Apellido')
    dni = models.PositiveIntegerField(validators=[MinValueValidator(1000000),MaxValueValidator(99999999)],verbose_name='DNI')  # Limitar numeros
    birth = models.DateField(null=True,verbose_name='Fecha de Nacimiento')
    role = models.CharField(max_length=1, choices=(('r', 'Referente'), ('f', 'Familiar')))


class Referring(models.Model):
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, related_name='referentes', null=True, verbose_name='Barrio')
    phone = models.PositiveIntegerField(verbose_name='Número de Teléfono')  # Limitar numero de telefono
    adress = models.CharField(max_length=80,verbose_name='Dirección')
    family = models.OneToOneField(Family, on_delete=models.CASCADE)
    last_buy = models.DateTimeField(null=True)
    family_last_buy = models.CharField(max_length=65, null=True)


class TypesProducts(models.Model):
    name = models.CharField(max_length=30)
    unit_measure = models.CharField(max_length=10, choices=UNITS_MEASURE,verbose_name='Unidad de Medida')
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class SortProducts(models.Model):
    types = models.ForeignKey(TypesProducts,null = True,on_delete=models.SET_NULL,verbose_name='Tipos de Producto')
    quantity = models.IntegerField(default=0,verbose_name='Cantidad')
