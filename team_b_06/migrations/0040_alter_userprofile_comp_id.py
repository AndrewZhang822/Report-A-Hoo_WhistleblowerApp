# Generated by Django 5.0.2 on 2024-04-28 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team_b_06', '0039_alter_report_mnemonic_alter_report_reported_comp_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='comp_id',
            field=models.CharField(default='', max_length=30),
        ),
    ]