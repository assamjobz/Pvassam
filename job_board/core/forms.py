from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Organization, JobPost, Application

class JobSeekerSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.user_type = 'job_seeker'
        if commit:
            user.save()
        return user

class OrganizationSignUpForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput())

    class Meta:
        model = Organization
        fields = ('name', 'description', 'website')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    def save(self, commit=True):
        user = User.objects.create_user(
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            user_type='organization'
        )
        organization = super().save(commit=False)
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
