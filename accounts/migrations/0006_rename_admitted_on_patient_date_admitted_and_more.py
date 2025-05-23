# Generated by Django 5.2 on 2025-04-15 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_patient_admitted_on_patient_diagnosed_with_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patient',
            old_name='admitted_on',
            new_name='date_admitted',
        ),
        migrations.RenameField(
            model_name='patient',
            old_name='discharged_on',
            new_name='date_discharged',
        ),
        migrations.RenameField(
            model_name='patient',
            old_name='doctor_in_charge',
            new_name='doctor_incharge',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='diagnosed_with',
        ),
        migrations.AddField(
            model_name='patient',
            name='admitted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='patient',
            name='diagnosis',
            field=models.TextField(default='severely-ill'),
            preserve_default=False,
        ),
    ]
