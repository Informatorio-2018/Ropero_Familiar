# Generated by Django 2.1.1 on 2018-12-31 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donaciones', '0052_auto_20181227_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.PositiveIntegerField(null=True, verbose_name='Numero de telefono'),
        ),
    ]