# Generated by Django 5.0.2 on 2024-03-26 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team_b_06', '0013_remove_report_user_id_report_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='status',
            field=models.CharField(default='New', max_length=100),
        ),
    ]
