# Generated by Django 4.2 on 2023-05-19 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appTienda', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='proNombre',
            field=models.CharField(max_length=45),
        ),
    ]
