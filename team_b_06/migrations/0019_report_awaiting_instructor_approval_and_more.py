# Generated by Django 5.0.2 on 2024-04-11 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team_b_06', '0018_rename_staff_approved_report_instructor_approved_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='awaiting_instructor_approval',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='comp_id',
            field=models.CharField(default='', max_length=10),
        ),
    ]