from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Organization, JobPost, Application

class JobSeekerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'job_seeker'
        if commit:
            user.save()
        return user

class OrganizationSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Organization
        fields = ('name', 'description', 'website')

    def save(self, commit=True):
        organization = super().save(commit=False)
        user = User.objects.create_user(
            username=self.cleaned_data['name'], # using name as username
            password=self.cleaned_data['password'],
            user_type='organization'
        )
        organization.user = user
        if commit:
            organization.save()
        return organization

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ('title', 'description', 'requirements', 'location')

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('cover_letter',)
