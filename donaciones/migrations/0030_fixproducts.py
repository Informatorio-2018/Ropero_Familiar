# Generated by Django 2.1.1 on 2018-12-02 23:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donaciones', '0029_merge_20181201_1101'),
    ]

    operations = [
        migrations.CreateModel(
            name='FixProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('quantity', models.DecimalField(decimal_places=2, default=0, max_digits=8, validators=[django.core.validators.MaxValueValidator(99999999.0), django.core.validators.MinValueValidator(0.0)], verbose_name='Cantidad')),
                ('unit_measure', models.CharField(choices=[('kg', 'Kg'), ('par', 'Par'), ('un', 'Unidad'), ('lt', 'Litro')], max_length=10, verbose_name='Unidad de Medida')),
            ],
        ),
    ]