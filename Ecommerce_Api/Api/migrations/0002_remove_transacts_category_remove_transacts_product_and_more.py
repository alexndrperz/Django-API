# Generated by Django 4.1.7 on 2023-04-04 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transacts',
            name='category',
        ),
        migrations.RemoveField(
            model_name='transacts',
            name='product',
        ),
        migrations.RemoveField(
            model_name='transacts',
            name='seller',
        ),
    ]
