# Generated by Django 4.0.5 on 2022-06-20 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hood', '0006_neighbourhood_occupants'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='neighbourhood',
            name='occupants',
        ),
        migrations.AddField(
            model_name='neighbourhood',
            name='occupants',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
