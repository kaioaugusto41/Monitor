# Generated by Django 4.0.4 on 2022-05-12 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0002_producao'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paradas_tipos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo_parada', models.CharField(max_length=300)),
                ('descricao_parada', models.TextField()),
            ],
        ),
    ]
