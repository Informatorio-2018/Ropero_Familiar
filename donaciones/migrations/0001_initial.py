# Generated by Django 2.1.1 on 2019-02-06 12:47

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import donaciones.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Carry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('types', models.CharField(max_length=30, verbose_name='Tipo de Donación')),
                ('unit_measure', models.CharField(choices=[('kg', 'Kg'), ('par', 'Par'), ('un', 'Unidad'), ('lt', 'Litro')], max_length=10, verbose_name='Unidad de Medida')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='Cantidad')),
                ('quantity_back', models.DecimalField(decimal_places=2, default=0, max_digits=6, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='Cantidad devolver')),
            ],
        ),
        migrations.CreateModel(
            name='DetailsDonation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('donation_type', models.CharField(max_length=30, verbose_name='Tipo de Donación')),
                ('unit_measure', models.CharField(choices=[('kg', 'Kg'), ('par', 'Par'), ('un', 'Unidad'), ('lt', 'Litro')], max_length=10, verbose_name='Unidad de Medida')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='Cantidad')),
            ],
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=80, verbose_name='Nombre o Razón Social')),
                ('ticket_number', models.PositiveIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99999999)], verbose_name='Numero de Recibo')),
            ],
        ),
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lastname', models.CharField(max_length=30, verbose_name='Apellido')),
                ('firstname', models.CharField(max_length=30, verbose_name='Nombre')),
                ('dni', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1000000), django.core.validators.MaxValueValidator(99999999)], verbose_name='DNI')),
                ('birth', models.DateField(null=True, verbose_name='Fecha de Nacimiento')),
                ('role', models.CharField(choices=[('r', 'Referente'), ('f', 'Familiar')], max_length=1)),
                ('ref', models.IntegerField(null=True)),
            ],
            options={
                'ordering': ['lastname'],
            },
        ),
        migrations.CreateModel(
            name='FamilyEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_entry', models.DateTimeField(auto_now_add=True)),
                ('familiar', models.CharField(max_length=65, null=True)),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingresos_familias', to='donaciones.Family')),
            ],
        ),
        migrations.CreateModel(
            name='FixProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, default=0, max_digits=8, validators=[django.core.validators.MaxValueValidator(99999999.0), django.core.validators.MinValueValidator(0.0)], verbose_name='Cantidad')),
            ],
        ),
        migrations.CreateModel(
            name='Neighborhood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Nombre del barrio')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='OtherDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=80, verbose_name='Descripción')),
                ('detailsdonation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='donaciones.DetailsDonation')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.PositiveIntegerField(null=True, verbose_name='Numero de telefono')),
                ('image', models.ImageField(blank=True, null=True, upload_to=donaciones.models.custom_upload_to, verbose_name='Imagen')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Referring',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.PositiveIntegerField(verbose_name='Número de Teléfono')),
                ('adress', models.CharField(max_length=80, verbose_name='Dirección')),
                ('last_buy', models.DateField(null=True)),
                ('family_last_buy', models.CharField(max_length=65, null=True)),
                ('family', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='donaciones.Family')),
                ('neighborhood', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='referentes', to='donaciones.Neighborhood', verbose_name='Barrio')),
            ],
        ),
        migrations.CreateModel(
            name='ResponsableFix',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30, verbose_name='Nombre')),
                ('lastname', models.CharField(max_length=30, verbose_name='Apellido')),
                ('phone', models.IntegerField()),
                ('adress', models.CharField(max_length=80, verbose_name='Dirección')),
                ('state', models.BooleanField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.IntegerField()),
                ('entry', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='donaciones.FamilyEntry')),
            ],
        ),
        migrations.CreateModel(
            name='SalesDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_type', models.CharField(max_length=30)),
                ('unit_measure', models.CharField(max_length=10)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='Cantidad')),
                ('price', models.IntegerField()),
                ('total', models.IntegerField()),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='donaciones.Sale')),
            ],
        ),
        migrations.CreateModel(
            name='SortProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, default=0, max_digits=8, validators=[django.core.validators.MaxValueValidator(99999999.0), django.core.validators.MinValueValidator(0.0)], verbose_name='Cantidad')),
            ],
        ),
        migrations.CreateModel(
            name='TypesDonation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Nombre')),
                ('unit_measure', models.CharField(choices=[('kg', 'Kg'), ('par', 'Par'), ('un', 'Unidad'), ('lt', 'Litro')], max_length=10, verbose_name='Unidad de Medida')),
                ('quantity_total', models.DecimalField(decimal_places=2, default=0, max_digits=8, validators=[django.core.validators.MaxValueValidator(99999999), django.core.validators.MinValueValidator(0)], verbose_name='Cantidad Total')),
            ],
        ),
        migrations.CreateModel(
            name='TypesFix',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Nombre')),
                ('unit_measure', models.CharField(choices=[('kg', 'Kg'), ('par', 'Par'), ('un', 'Unidad'), ('lt', 'Litro')], max_length=10, verbose_name='Unidad de Medida')),
                ('quantity_total', models.DecimalField(decimal_places=2, default=0, max_digits=8, validators=[django.core.validators.MaxValueValidator(99999999), django.core.validators.MinValueValidator(0)], verbose_name='Cantidad Total')),
            ],
        ),
        migrations.CreateModel(
            name='TypesProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('unit_measure', models.CharField(choices=[('kg', 'Kg'), ('par', 'Par'), ('un', 'Unidad'), ('lt', 'Litro')], max_length=10, verbose_name='Unidad de Medida')),
                ('price', models.IntegerField(default=0)),
                ('quantity_total', models.DecimalField(decimal_places=2, default=0, max_digits=8, validators=[django.core.validators.MaxValueValidator(99999999.0), django.core.validators.MinValueValidator(0.0)], verbose_name='Cantidad Total')),
            ],
        ),
        migrations.AddField(
            model_name='sortproducts',
            name='types',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='donaciones.TypesProducts', verbose_name='Tipos de Producto'),
        ),
        migrations.AddField(
            model_name='fixproducts',
            name='responsable',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='donaciones.ResponsableFix'),
        ),
        migrations.AddField(
            model_name='fixproducts',
            name='types',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='donaciones.TypesFix', verbose_name='Tipos de Producto'),
        ),
        migrations.AddField(
            model_name='detailsdonation',
            name='donation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detailsdonation', to='donaciones.Donation'),
        ),
        migrations.AddField(
            model_name='carry',
            name='responsable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable', to='donaciones.ResponsableFix'),
        ),
    ]
