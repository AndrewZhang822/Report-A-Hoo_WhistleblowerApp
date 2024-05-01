from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserCreationForm, LoginForm, SignupForm, ReportForm, ResolveReportForm, ProfileForm
from django.urls import reverse_lazy
from django.views import generic
from django.template import loader
from django.utils import timezone
from .models import *
from django.core.exceptions import PermissionDenied
from .models import Report
from django.shortcuts import get_object_or_404
from django.conf import settings
import boto3

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

def home(request):
    return render(request, 'project_b_06/home.html')

@login_required
def profile(request):
    if request.user.is_authenticated:
        if request.user.profile.site_admin == False:
            reports = Report.objects.filter(user=request.user.profile)
        else:
            reports = Report.objects.none()
    else:
        reports = Report.objects.none()
    return render(request, 'project_b_06/profile.html', {'user_profile': request.user.profile, 'user':request.user, 'reports':reports})


def signin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('add_details')
            else:
                # Add an explicit error message if authentication fails
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            request.user.role = form.cleaned_data.get('role')
            user = form.save()
            profile = user.profile
            profile.role = form.cleaned_data['role']
            profile.comp_id = form.cleaned_data['password']
            profile.save()
            return redirect('login')
        else:
            return render(request, 'account/signup.html', {'form': form})
    else:
        form = SignupForm()
    return render(request, 'account/signup.html',{'form': form})

def add_details(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)

    # if user already has set their computing id, redirect to profile page
    if user.profile.comp_id:
        return redirect('profile')

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=user.profile)
    return render(request, 'account/add_details.html', {'form': form})

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        form.fields.pop('comp_id', None)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm(instance=request.user.profile)
        form.fields.pop('comp_id', None)
    
    if request.user.is_authenticated:
        if request.user.profile.site_admin == False:
            reports = Report.objects.filter(user=request.user.profile)
        else:
            reports = Report.objects.none()
    else:
        reports = Report.objects.none()

    user_profile = request.user.profile
    context = {
        'form': form,
        'user_profile': user_profile,
        'reports': reports,
    }
    return render(request, 'project_b_06/profile.html', context)


def admin_login(request):
    return render(request, 'admin:index')
def logout_view(request):
    logout(request)
    return redirect('home')

def report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            mnemonic = form.cleaned_data['mnemonic']
            number = form.cleaned_data['number']
            reported_fname = form.cleaned_data['reported_fname']
            reported_lname = form.cleaned_data['reported_lname']
            reported_comp_id = form.cleaned_data['reported_comp_id']
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            whisteblower_approved = form.cleaned_data['whisteblower_approved']
            admin_approved = False
            staff_approved = False
            pub_date = timezone.now()
            file = form.cleaned_data['file']
            tag = form.cleaned_data['tag']

            if request.user.is_authenticated:
                user = request.user.profile
                reporter_comp_id = user.comp_id
            else:
                user = None
                reporter_comp_id = 'Anonymous'
                
            report = Report(
                mnemonic=mnemonic,
                number=number,
                reported_fname=reported_fname,
                reported_lname=reported_lname,
                reported_comp_id=reported_comp_id,
                reporter_comp_id = reporter_comp_id,
                whisteblower_approved=whisteblower_approved,
                title=title,
                text=text,
                pub_date=pub_date,
                file=file,
                user=user,
                tag=tag
            )
            report.save()
            return redirect('confirmation')  
        else:
            return render(request, 'project_b_06/report.html', {'form': form})
    else:
        form = ReportForm()
    return render(request, 'project_b_06/report.html',  {'form': form})

def confirmation(request):
    latest_report = Report.objects.order_by("-pub_date").first()
    context = { "latest_report": latest_report }
    return render(request, 'project_b_06/confirmation.html', context)

def view_reports(request):
    if request.user.is_authenticated:
        if request.user.profile.site_admin:
            reports = Report.objects.all()
        else:
            reports = Report.objects.filter(whisteblower_approved=True)
    else:
        reports = Report.objects.filter(whisteblower_approved=True)

    return render(request, 'project_b_06/view_reports.html', {'reports': reports})

def report_detail(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    if (request.user.is_authenticated):
        if (request.user.profile.site_admin):
            if report.status == ("New"):
                report.status = "In Progress"
                report.save(update_fields=['status'])

    if report.file:  # Check if a file is associated with the report
        url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/static/reports/{report.file.name}"
    else:
        url = None  # No file is associated with the report
    is_admin = False
    if request.user.is_authenticated:
        is_admin = request.user.profile.site_admin
    public = report.whisteblower_approved

    return render(request, 'project_b_06/report_detail.html', {'report': report, 'url': url, 'is_admin': is_admin, 'public': public, 'is_authenticated': request.user.is_authenticated})

def report_approve(request, report_id):
    report = get_object_or_404(Report, id=report_id)

    report.admin_approved = True
    report.save()

    return redirect('view_reports')

def send_instructor(request, report_id):
    report = get_object_or_404(Report, id=report_id)

    report.awaiting_instructor_approval = True
    report.save()

    return redirect('view_reports')

def instructor_approve(request, report_id):
    report = get_object_or_404(Report, id=report_id)

    if request.user.is_authenticated and report.reported_comp_id == request.user.profile.comp_id:
        report.instructor_approved = True
        report.save()

    return redirect('instructor_reports')

def submission_history(request):
    if request.user.is_authenticated:
        if request.user.profile.site_admin == False:
            reports = Report.objects.filter(user=request.user.profile)
        else:
            reports = Report.objects.none()
    else:
        reports = Report.objects.none()
    return render(request, 'project_b_06/submission_history.html', {'reports': reports})

def delete_report(request, report_id):
    report = Report.objects.get(pk=report_id)
    if request.method == 'POST':
        report = get_object_or_404(Report, id=report_id)
        if request.user.is_authenticated and report.user == request.user.profile:
            report.delete()
            return redirect('profile')
        else:
            raise PermissionDenied("You are not authorized to delete this submission.")
    else:
        pass

def resolve_report(request, report_id):
    report = Report.objects.get(pk=report_id)
    if request.method == 'POST':
        form = ResolveReportForm(request.POST)
        if form.is_valid():
            report.status = "Resolved"
            report.note = form.cleaned_data['note']
            report.save(update_fields = ['status', 'note'])
            return redirect('view_reports')
    else:
        form = ResolveReportForm()
    return render(request, "project_b_06/resolve_report.html", {'report': report, 'form': form})

def public_reports(request):
    reports = Report.objects.filter(whisteblower_approved=True, admin_approved=True, instructor_approved=True)
    return render(request, 'project_b_06/public_reports.html', {'reports': reports})

def instructor_reports(request):
    reports = Report.objects.filter(awaiting_instructor_approval=True, reported_comp_id=request.user.profile.comp_id)
    return render(request, 'project_b_06/instructor_reports.html', {'reports': reports})