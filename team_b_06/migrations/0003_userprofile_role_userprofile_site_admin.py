# Generated by Django 5.0.2 on 2024-03-16 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team_b_06', '0002_alter_userprofile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.CharField(default='student', max_length=30),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='site_admin',
            field=models.BooleanField(default=False),
        ),
    ]