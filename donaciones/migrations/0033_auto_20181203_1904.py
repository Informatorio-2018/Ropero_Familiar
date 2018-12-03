# Generated by Django 2.1.1 on 2018-12-03 22:04

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('donaciones', '0032_responsablefix_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('types', models.CharField(max_length=30, verbose_name='Tipo de Donación')),
                ('unit_measure', models.CharField(choices=[('kg', 'Kg'), ('par', 'Par'), ('un', 'Unidad'), ('lt', 'Litro')], max_length=10, verbose_name='Unidad de Medida')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='Cantidad')),
            ],
        ),
        migrations.RemoveField(
            model_name='responsablefix',
            name='quantity',
        ),
        migrations.AddField(
            model_name='responsablefix',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='responsablefix',
            name='phone',
            field=models.IntegerField(),
        ),
        migrations.AddField(
            model_name='carry',
            name='responsable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable', to='donaciones.ResponsableFix'),
        ),
    ]