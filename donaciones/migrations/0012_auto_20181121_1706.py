# Generated by Django 2.1.1 on 2018-11-21 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('donaciones', '0011_auto_20181121_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='referring',
            name='family',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='donaciones.Family'),
        ),
        migrations.AlterField(
            model_name='family',
            name='ref',
            field=models.IntegerField(null=True),
        ),
    ]
