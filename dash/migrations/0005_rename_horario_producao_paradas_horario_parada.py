# Generated by Django 4.0.4 on 2022-05-12 01:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0004_paradas'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paradas',
            old_name='horario_producao',
            new_name='horario_parada',
        ),
    ]
