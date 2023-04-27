# Generated by Django 4.1.7 on 2023-04-27 13:16

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0017_alter_invitationcodes_expire_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitationcodes',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 4, 13, 15, 59, 383617, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='invitationcodes',
            name='invitationCodes',
            field=models.CharField(default='gYfP4Jbokzo8IMm', max_length=15, unique=True),
        ),
        migrations.CreateModel(
            name='RoleRequests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_role', models.BooleanField()),
                ('is_password', models.BooleanField()),
                ('message', models.CharField(max_length=100)),
                ('approved', models.BooleanField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
