# Generated by Django 2.1.1 on 2018-11-21 18:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('donaciones', '0009_auto_20181121_1311'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='referring',
            name='family',
        ),
        migrations.AddField(
            model_name='family',
            name='ref_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='donaciones.Referring'),
        ),
    ]
