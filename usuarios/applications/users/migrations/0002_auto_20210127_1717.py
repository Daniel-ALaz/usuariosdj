# Generated by Django 3.1.5 on 2021-01-27 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='apellidos',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='nombres',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
