from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    home,
    JobSeekerSignUpView,
    OrganizationSignUpView,
    JobPostCreateView,
    JobPostUpdateView,
    JobPostDeleteView,
    OrganizationJobListView,
    JobPostListView,
    JobPostDetailView,
    ApplicationCreateView,
)

urlpatterns = [
    path('', home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/jobseeker/', JobSeekerSignUpView.as_view(), name='jobseeker_signup'),
    path('signup/organization/', OrganizationSignUpView.as_view(), name='organization_signup'),
    path('jobs/', JobPostListView.as_view(), name='job_list'),
    path('jobs/new/', JobPostCreateView.as_view(), name='job_post_create'),
    path('jobs/<int:pk>/', JobPostDetailView.as_view(), name='job_post_detail'),
    path('jobs/<int:pk>/edit/', JobPostUpdateView.as_view(), name='job_post_update'),
    path('jobs/<int:pk>/delete/', JobPostDeleteView.as_view(), name='job_post_delete'),
    path('jobs/<int:pk>/apply/', ApplicationCreateView.as_view(), name='apply_job'),
    path('organization/jobs/', OrganizationJobListView.as_view(), name='organization_jobs'),
]
