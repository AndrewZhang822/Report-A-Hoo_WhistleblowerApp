# Generated by Django 5.0.2 on 2024-03-19 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team_b_06', '0010_report_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user_type',
        ),
    ]