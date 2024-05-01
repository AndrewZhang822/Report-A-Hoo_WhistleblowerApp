from django.urls import path
from . import views
from django.urls import path
from .views import profile, SignUpView, add_details, profile_view
from django.contrib import admin


urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/profile/', profile_view, name='profile'),
    path('accounts/login/', views.signin, name='login'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('report/', views.report, name='report'),
    path('report/confirmation/', views.confirmation, name='confirmation'),
    path('reports/', views.view_reports, name='view_reports'),
    path('report/<int:report_id>/', views.report_detail, name='report_detail'),
    path('report/delete/<int:report_id>/', views.delete_report, name='delete_report'),
    path('report/<int:report_id>/approve/', views.report_approve, name='report_approve'),
    path('report/<int:report_id>/instructor', views.instructor_approve, name='instructor_approve'),
    path('report/<int:report_id>/send', views.send_instructor, name='send_instructor'),
    path('submission_history/', views.submission_history, name='submission_history'),
    path('resolve/<int:report_id>/', views.resolve_report, name = "resolve_report"), 
    path('public_reports/', views.public_reports, name='public_reports'),
    path('instructor_reports/', views.instructor_reports, name='instructor_reports'),
    path('account/add_details/', add_details, name='add_details'),
]