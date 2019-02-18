from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
import decimal
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from PIL import Image


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
    quantity_total = models.DecimalField(max_digits=8, decimal_places=2, default=0, validators=[MaxValueValidator(99999999), MinValueValidator(0)], verbose_name='Cantidad Total')

    def __str__(self):
        return self.name


class Neighborhood(models.Model):
    name = models.CharField(max_length=30, verbose_name="Nombre del barrio")

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        ordering = ["name"]


class Family(models.Model):
    lastname = models.CharField(max_length=30, verbose_name='Apellido')
    firstname = models.CharField(max_length=30, verbose_name='Nombre')
    dni = models.PositiveIntegerField(validators=[MinValueValidator(1000000), MaxValueValidator(99999999)], verbose_name='DNI')  # Limitar numeros
    birth = models.DateField(null=True, verbose_name='Fecha de Nacimiento')
    role = models.CharField(max_length=1, choices=(('r', 'Referente'), ('f', 'Familiar')))
    ref = models.IntegerField(null=True)

    def __str__(self):
        return "%s, %s" % (self.lastname, self.firstname)

    class Meta:
        ordering = ["lastname"]


class FamilyEntry(models.Model):
    last_entry = models.DateField(auto_now_add=True, null=True)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='ingresos_familias')


class Referring(models.Model):
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, related_name='referentes', null=True, verbose_name='Barrio')
    phone = models.PositiveIntegerField(verbose_name='Número de Teléfono')  # Limitar numero de telefono
    adress = models.CharField(max_length=80, verbose_name='Dirección')
    family = models.OneToOneField(Family, on_delete=models.CASCADE, null=True)
    last_buy = models.DateField(null=True)
    family_last_buy = models.CharField(max_length=65, null=True)

    def __str__(self):
        return "{}-{}-{}".format(self.family.lastname, self.family.firstname, self.last_buy)


class TypesProducts(models.Model):
    name = models.CharField(max_length=30)
    unit_measure = models.CharField(max_length=10, choices=UNITS_MEASURE, verbose_name='Unidad de Medida')
    price = models.IntegerField(default=0,verbose_name='Precio')
    quantity_total = models.DecimalField(max_digits=8, decimal_places=2, default=0, validators=[MaxValueValidator(99999999.00), MinValueValidator(0.00)], verbose_name='Cantidad Total')

    def __str__(self):
        return self.name


class ResponsableFix(models.Model):
    name = models.CharField(max_length=30, verbose_name='Nombre')
    lastname = models.CharField(max_length=30, verbose_name='Apellido')
    phone = models.IntegerField(verbose_name='Telefono')
    adress = models.CharField(max_length=80, verbose_name='Dirección')
    state = models.BooleanField(default=0)

    def __str__(self):
        return self.name

    # neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, related_name='referentes', null=True, verbose_name='Barrio')


class Carry(models.Model):
    date = models.DateTimeField(null=True,auto_now_add=True,verbose_name="Fecha de creacion")
    types = models.CharField(max_length=30, verbose_name='Tipo de Donación')
    unit_measure = models.CharField(max_length=10, choices=UNITS_MEASURE, verbose_name='Unidad de Medida')
    quantity = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.01)], verbose_name='Cantidad')
    quantity_back = models.DecimalField(default=0, max_digits=6, decimal_places=2, validators=[MinValueValidator(0.01)], verbose_name='Cantidad devolver')
    responsable = models.ForeignKey(ResponsableFix, on_delete=models.CASCADE, related_name='responsable')

    def __str__(self):
        return self.responsable.name


class SortProducts(models.Model):
    types = models.ForeignKey(TypesProducts, null=True, on_delete=models.SET_NULL, verbose_name='Tipos de Producto')
    quantity = models.DecimalField(max_digits=8, decimal_places=2, default=0, validators=[MaxValueValidator(99999999.00), MinValueValidator(0.00)], verbose_name='Cantidad')


class TypesFix(models.Model):
    name = models.CharField(max_length=30, verbose_name='Nombre')
    unit_measure = models.CharField(max_length=10, choices=UNITS_MEASURE, verbose_name='Unidad de Medida')
    quantity_total = models.DecimalField(max_digits=8, decimal_places=2, default=0, validators=[MaxValueValidator(99999999), MinValueValidator(0)], verbose_name='Cantidad Total')

    def __str__(self):
        return self.name


class FixProducts(models.Model):
    types = models.ForeignKey(TypesFix, null=True, on_delete=models.SET_NULL, verbose_name='Tipos de Producto')
    quantity = models.DecimalField(max_digits=8, decimal_places=2, default=0, validators=[MaxValueValidator(99999999.00), MinValueValidator(0.00)], verbose_name='Cantidad')
    responsable = models.OneToOneField(ResponsableFix, null=True, on_delete=models.CASCADE)


class FamilyEntry(models.Model):
    last_entry = models.DateTimeField(auto_now_add=True)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='ingresos_familias')
    familiar = models.CharField(max_length=65, null=True)  # Preguntar a Matias

    def __str__(self):
        return "{}, {}".format(self.family.lastname, self.family.firstname)


class Sale(models.Model):
    total = models.IntegerField()
    entry = models.OneToOneField(FamilyEntry, on_delete=models.CASCADE)


class SalesDetails(models.Model):
    product_type = models.CharField(max_length=30)
    unit_measure = models.CharField(max_length=10)
    quantity = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.01)], verbose_name='Cantidad')
    price = models.IntegerField()
    total = models.IntegerField()
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='sales')


# Borra la imagen anterior del perfil
def custom_upload_to(instance, filename):
    old_instance = Profile.objects.get(pk=instance.pk)
    old_instance.image.delete()
    return 'profile_pics/' + filename


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.PositiveIntegerField(verbose_name='Numero de telefono', null=True)
    image = models.ImageField(verbose_name='Imagen', upload_to=custom_upload_to, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Perfil'

    def save(self, **kwargs):
        super().save()
        if self.image:
            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img = img.resize(output_size, Image.ANTIALIAS)
                img.save(self.image.path)


@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    if kwargs.get('created', False):
        # print(instance.id)
        # instance.username = instance.username.upper()
        # # instance.save()
        Profile.objects.get_or_create(user=instance)
        print("Se acaba de crear un usuario y su perfil enlazado")


# class ListSort(models.Model):
#     name=models.CharField(max_length=30)
#     quantity_total = models.IntegerField(default=0, verbose_name='Cantidad Total')

#     def __str__(self):
#         return self.name
