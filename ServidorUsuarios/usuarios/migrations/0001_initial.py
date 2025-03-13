# Generated by Django 5.1.7 on 2025-03-13 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('celular', models.IntegerField(max_length=15)),
                ('correo', models.CharField(max_length=200)),
                ('cedula', models.CharField(max_length=12)),
                ('edad', models.CharField(max_length=3)),
                ('eventos', models.JSONField(blank=True, default=list)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
