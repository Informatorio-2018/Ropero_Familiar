# Generated by Django 2.1.1 on 2018-11-28 19:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('donaciones', '0020_merge_20181128_1558'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SalesDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_type', models.CharField(max_length=30)),
                ('unit_measure', models.CharField(choices=[('kg', 'Kg'), ('par', 'Par'), ('un', 'Unidad'), ('lt', 'Litro')], max_length=10)),
                ('quantity', models.IntegerField()),
                ('price', models.IntegerField()),
                ('total', models.IntegerField()),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='donaciones.Sale')),
            ],
        ),
        migrations.RenameField(
            model_name='familyentry',
            old_name='last_buy',
            new_name='last_entry',
        ),
        migrations.AddField(
            model_name='sale',
            name='entry',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='donaciones.FamilyEntry'),
        ),
    ]