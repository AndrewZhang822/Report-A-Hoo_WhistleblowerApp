# Generated by Django 5.0.2 on 2024-03-05 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team_b_06', '0003_report'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='reported_lName',
            new_name='reported_lname',
        ),
        migrations.AddField(
            model_name='report',
            name='visibility',
            field=models.BooleanField(default=False),
        ),
    ]
