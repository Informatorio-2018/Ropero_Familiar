from django.core.validators import MaxValueValidator, MinValueValidator
import decimal
from django.db import models

# Create your models here.
UNITS_MEASURE = (('kg', 'Kg'), ('par', 'Par'), ('un', 'Unidad'), ('lt', 'Litro'))


class Donation(models.Model):
    date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=80, verbose_name='Nombre o Razón Social')
    ticket_number = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(99999999)], null=True, verbose_name='Numero de Recibo')

    def __str__(self):
        return self.name


class DetailsDonation(models.Model):
    donation_type = models.CharField(max_length=30, verbose_name='Tipo de Donación')
    unit_measure = models.CharField(max_length=10, choices=UNITS_MEASURE, verbose_name='Unidad de Medida')
    quantity = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.01)], verbose_name='Cantidad')
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name='detailsdonation')

    def __str__(self):
        return self.donation_type


class OtherDetail(models.Model):
    description = models.CharField(max_length=80, verbose_name='Descripción')
    detailsdonation = models.OneToOneField(DetailsDonation, on_delete=models.CASCADE)


class TypesDonation(models.Model):
    name = models.CharField(max_length=30, verbose_name='Nombre')
    unit_measure = models.CharField(max_length=10, choices=UNITS_MEASURE, verbose_name='Unidad de Medida')
    quantity_total = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Cantidad Total')

    def __str__(self):
        return self.name


class Neighborhood(models.Model):
    name = models.CharField(max_length=30, verbose_name="Nombre del barrio")

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        ordering=["name"]


class Family(models.Model):
    lastname = models.CharField(max_length=30, verbose_name='Apellido')
    firstname = models.CharField(max_length=30, verbose_name='Nombre')
    dni = models.PositiveIntegerField(validators=[MinValueValidator(1000000), MaxValueValidator(99999999)], verbose_name='DNI')  # Limitar numeros
    birth = models.DateField(null=True, verbose_name='Fecha de Nacimiento')
    role = models.CharField(max_length=1, choices=(('r', 'Referente'), ('f', 'Familiar')))
    ref = models.IntegerField(null=True)

    def __str__(self):
        return "%s, %s" %(self.lastname,self.firstname)

    class Meta:
        ordering = ["lastname"]

class Referring(models.Model):
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, related_name='referentes', null=True, verbose_name='Barrio')
    phone = models.PositiveIntegerField(verbose_name='Número de Teléfono')  # Limitar numero de telefono
    adress = models.CharField(max_length=80, verbose_name='Dirección')
    family = models.OneToOneField(Family, on_delete=models.CASCADE, null=True)
    last_buy = models.DateField(null=True)
    family_last_buy = models.CharField(max_length=65, null=True)


class TypesProducts(models.Model):
    name = models.CharField(max_length=30)
    unit_measure = models.CharField(max_length=10, choices=UNITS_MEASURE, verbose_name='Unidad de Medida')
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class SortProducts(models.Model):
    types = models.ForeignKey(TypesProducts, null=True, on_delete=models.SET_NULL, verbose_name='Tipos de Producto')
    quantity = models.IntegerField(verbose_name='Cantidad')

    def __str__(self):
        return self.types.name

class FamilyEntry(models.Model):
    last_entry = models.DateTimeField(auto_now_add=True)
    family = models.ForeignKey(Family,on_delete=models.CASCADE, related_name='ingresos_familias')
    familiar = models.CharField(max_length=65,null=True)#Preguntar a Matias


# class ListSort(models.Model):
#     name=models.CharField(max_length=30)
#     quantity_total = models.IntegerField(default=0, verbose_name='Cantidad Total')

#     def __str__(self):
#         return self.name
