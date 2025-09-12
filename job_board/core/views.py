from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import User, JobPost, Application
from .forms import JobSeekerSignUpForm, OrganizationSignUpForm, JobPostForm, ApplicationForm


def home(request):
    jobs = JobPost.objects.filter(organization__is_verified=True).order_by('-created_at')[:5]
    return render(request, 'home.html', {'jobs': jobs})

class JobSeekerSignUpView(CreateView):
    model = User
    form_class = JobSeekerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'job_seeker'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        return redirect('home')

class OrganizationSignUpView(CreateView):
    model = User
    form_class = OrganizationSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'organization'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.save()
        return redirect('home')


class VerifiedOrganizationRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.user_type == 'organization' and self.request.user.organization.is_verified

class JobSeekerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.user_type == 'job_seeker'

class JobPostCreateView(VerifiedOrganizationRequiredMixin, CreateView):
    model = JobPost
    form_class = JobPostForm
    template_name = 'job_post_form.html'
    success_url = reverse_lazy('organization_jobs')

    def form_valid(self, form):
        form.instance.organization = self.request.user.organization
        return super().form_valid(form)

class JobPostUpdateView(VerifiedOrganizationRequiredMixin, UpdateView):
    model = JobPost
    form_class = JobPostForm
    template_name = 'job_post_form.html'
    success_url = reverse_lazy('organization_jobs')

class JobPostDeleteView(VerifiedOrganizationRequiredMixin, DeleteView):
    model = JobPost
    template_name = 'job_post_confirm_delete.html'
    success_url = reverse_lazy('organization_jobs')

class OrganizationJobListView(VerifiedOrganizationRequiredMixin, ListView):
    model = JobPost
    template_name = 'organization_job_list.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return JobPost.objects.filter(organization=self.request.user.organization)

class JobPostListView(ListView):
    model = JobPost
    template_name = 'job_post_list.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return JobPost.objects.filter(organization__is_verified=True).order_by('-created_at')

class JobPostDetailView(DetailView):
    model = JobPost
    template_name = 'job_post_detail.html'
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and self.request.user.user_type == 'job_seeker':
            context['has_applied'] = Application.objects.filter(job_post=self.object, applicant=self.request.user).exists()
        return context

class ApplicationCreateView(JobSeekerRequiredMixin, CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'application_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.job_post = get_object_or_404(JobPost, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.applicant = self.request.user
        form.instance.job_post = self.job_post
        form.save()
        return redirect('job_post_detail', pk=self.job_post.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = self.job_post
        return context
