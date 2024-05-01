# Generated by Django 5.0.2 on 2024-04-13 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team_b_06', '0021_alter_report_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='tag',
            field=models.CharField(choices=[('N', 'None'), ('GR', 'Grading'), ('AI', 'Accessibility and Inclusivity'), ('GF', 'General Feedback'), ('CC', 'Classroom Conduct/Behavior'), ('O', 'Other'), ('SM', 'Subject Material')], default='N', max_length=5000),
        ),
    ]