# Generated by Django 4.1.7 on 2023-03-27 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameProduct', models.CharField(max_length=50)),
                ('priceProduct', models.CharField(max_length=30)),
                ('dateReleased', models.DateField()),
            ],
        ),
    ]
