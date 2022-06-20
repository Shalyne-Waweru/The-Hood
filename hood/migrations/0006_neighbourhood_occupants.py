# Generated by Django 4.0.5 on 2022-06-20 08:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hood', '0005_alter_neighbourhood_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='neighbourhood',
            name='occupants',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]