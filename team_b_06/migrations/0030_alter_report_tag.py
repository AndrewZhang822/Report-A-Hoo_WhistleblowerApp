# Generated by Django 5.0.2 on 2024-04-13 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team_b_06', '0029_alter_report_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='tag',
            field=models.CharField(choices=[('GF', 'General Feedback'), ('CC', 'Classroom Conduct/Behavior'), ('SM', 'Subject Material'), ('GR', 'Grading'), ('AI', 'Accessibility and Inclusivity'), (None, 'None'), ('O', 'Other')], default=None, max_length=5000),
        ),
    ]
