# Generated by Django 5.0.2 on 2024-04-13 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team_b_06', '0019_report_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='tag',
            field=models.CharField(choices=[('CC', 'Classroom Conduct/Behavior'), ('AI', 'Accessibility and Inclusivity'), ('GR', 'Grading'), ('O', 'Other'), ('SM', 'Subject Material'), ('GF', 'General Feedback')], default='GF', max_length=5000),
        ),
    ]
