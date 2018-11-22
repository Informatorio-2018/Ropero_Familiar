# Generated by Django 2.1.1 on 2018-11-21 19:10

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('donaciones', '0008_merge_20181121_0912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='family',
            name='birth',
            field=models.DateField(null=True, verbose_name='Fecha de Nacimiento'),
        ),
        migrations.AlterField(
            model_name='family',
            name='dni',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1000000), django.core.validators.MaxValueValidator(99999999)], verbose_name='DNI'),
        ),
        migrations.AlterField(
            model_name='family',
            name='firstname',
            field=models.CharField(max_length=30, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='family',
            name='lastname',
            field=models.CharField(max_length=30, verbose_name='Apellido'),
        ),
        migrations.AlterField(
            model_name='referring',
            name='adress',
            field=models.CharField(max_length=80, verbose_name='Dirección'),
        ),
        migrations.AlterField(
            model_name='referring',
            name='neighborhood',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='referentes', to='donaciones.Neighborhood', verbose_name='Barrio'),
        ),
        migrations.AlterField(
            model_name='referring',
            name='phone',
            field=models.PositiveIntegerField(verbose_name='Número de Teléfono'),
        ),
        migrations.AlterField(
            model_name='sortproducts',
            name='types',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='donaciones.TypesProducts', verbose_name='Tipos de Producto'),
        ),
    ]
