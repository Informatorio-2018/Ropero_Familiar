# Generated by Django 2.1.1 on 2019-04-25 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donaciones', '0006_auto_20190320_0051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referring',
            name='phone',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Número de Teléfono'),
        ),
    ]
