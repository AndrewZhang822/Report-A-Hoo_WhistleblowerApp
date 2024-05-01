from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Report, UserProfile
import requests
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class SignupForm(UserCreationForm):
    ROLE_CHOICES = (
        ('Student', 'Student'),
        ('Instructor', 'Instructor')
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    class Meta:
        model = User
        # password is used for comp_id
        fields = ['username', 'password1', 'password2', 'role', 'password']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ProfileForm(forms.ModelForm):
    ROLE_CHOICES = (
        ('Student', 'Student'),
        ('Instructor', 'Instructor')
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    username = forms.CharField(required=True)
    comp_id = forms.CharField(required=True, label='Computing ID')

    class Meta:
        model = UserProfile
        fields = ['username', 'comp_id', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exclude(pk=self.instance.user.pk).exists():
            raise ValidationError("Username is already taken.")
        return username

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.cleaned_data['username']:
            profile.user.username = self.cleaned_data['username']
            profile.user.save()
        if commit:
            profile.save()
        return profile

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['mnemonic', 'number', 'reported_fname', 'reported_lname', 'reported_comp_id', 'whisteblower_approved', 'title', 'text', 'file', 'tag']

        widgets = {
            'tag': forms.Select(attrs={'class': 'form-control'}),
        }

        error_messages = {
            'mnemonic': {
                'required': "Please enter a value for your field: course mnemonic.",
                'max_length': "Please enter a valid value for your field. Mnemonic has to be <= 4 characters.",
                'invalid': "Please enter only letters for the course mnemonic.",
            },
            'number': {
                'required': "Please enter a value for your field: course number.",
                'invalid': "Please enter a valid value for your field. Number has to be <= 4 digits and contain no alphabetical or special characters.",
                'max_length': "Please enter a valid value for your field. Number has to be <= 4 digits and contain no alphabetical or special characters.",
            },
            'reported_fname': {
                'required': "Please enter a value for your field: first name.",
                'max_length': "Please enter a valid value for your field. First name has to be <= 20 characters.",
            },
            'reported_lname': {
                'required': "Please enter a value for your field: last name.",
                'max_length': "Please enter a valid value for your field. Last name has to be <= 20 characters.",
            },
            'reported_comp_id': {
                'required': "Please enter a value for your field: computing id.",
                'max_length': "Please enter a valid value for your field. Computing ID has to be <= 7 characters.",
            },
            'title': {
                'required': "Please enter a value for your field: report title.",
                'max_length': "Please enter a valid value for your field. Title has to be <= 100 characters.",
            },
            'text': {
                'required': "Please enter a value for your field: report text.",
                'max_length': "Please enter a valid value for your field. Text has to be <= 5000 characters.",
            }
        }

        #tag = forms.ChoiceField(choices = Report.TAG_CHOICES, initial="N", widget=forms.Select(attrs={'class': 'form-control'}))



class ResolveReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['note']