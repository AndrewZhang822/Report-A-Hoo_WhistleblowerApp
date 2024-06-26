# Generated by Django 5.0.2 on 2024-04-13 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team_b_06', '0034_alter_report_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='tag',
            field=models.CharField(choices=[(None, 'None'), ('CC', 'Classroom Conduct/Behavior'), ('GR', 'Grading'), ('SM', 'Subject Material'), ('AI', 'Accessibility and Inclusivity'), ('GF', 'General Feedback'), ('O', 'Other')], default=None, max_length=5000),
        ),
    ]
