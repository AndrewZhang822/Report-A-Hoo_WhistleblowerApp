from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator
import datetime
from django.core.validators import RegexValidator

alpha = RegexValidator(r'^[a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    role = models.CharField(max_length=30, default='Student')
    site_admin = models.BooleanField(default=False)
    comp_id = models.CharField(max_length=30, default='')

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Report(models.Model):
    TAG_CHOICES = (
        ("N", "None"),
        ("CC", "Classroom Conduct/Behavior"),
        ("GR", "Grading"),
        ("SM", "Subject Material"),
        ("AI", "Accessibility and Inclusivity"),
        ("GF", "General Feedback"),
        ("O", "Other")
    )

    mnemonic = models.CharField(max_length=4, validators=[alpha])
    number = models.IntegerField(default=0, validators=[MaxValueValidator(9999)])
    reported_fname = models.CharField(max_length=20)
    reported_lname = models.CharField(max_length=20)
    reported_comp_id = models.CharField(max_length=7, validators=[alphanumeric])
    reporter_comp_id = models.CharField(max_length=30, default='')
    #True is public, False is private
    whisteblower_approved = models.BooleanField(default=False)
    admin_approved = models.BooleanField(default=False)
    instructor_approved = models.BooleanField(default=False)
    awaiting_instructor_approval = models.BooleanField(default=False)
    text = models.CharField(max_length=5000)
    title = models.CharField(max_length=100, default = 'No Title (Default)')
    pub_date = models.DateTimeField("date published", default=timezone.now)
    file = models.FileField(upload_to='reports/', blank=True, null=True)
    user = models.ForeignKey(UserProfile, blank=True, null=True, on_delete=models.CASCADE) # user linked to report
    status = models.CharField(max_length=100, default="New")  # new, in progress, or resolved
    note = models.TextField(default="")
    submit_date = models.DateField(default=datetime.date.today)
    tag = models.CharField(max_length=5000, choices=TAG_CHOICES, default="N")
    def __str__(self):
        return   self.reported_comp_id
