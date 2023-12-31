# Generated by Django 4.2.7 on 2023-11-29 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agendabarberia', '0006_alter_barberia_titulo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barberia',
            name='titulo',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='barberia',
            name='ubicacion',
            field=models.CharField(choices=[('guayaquil', 'guayaquil'), ('santa-elena', 'santa-elena'), ('milagro', 'milagro'), ('duran', 'duran')], default='*', max_length=200),
        ),
    ]
