# Generated by Django 4.0.4 on 2022-05-18 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0005_rename_horario_producao_paradas_horario_parada'),
    ]

    operations = [
        migrations.CreateModel(
            name='Produtos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_produto', models.CharField(max_length=150)),
            ],
        ),
    ]