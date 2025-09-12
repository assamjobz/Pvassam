from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ("job_seeker", "Job Seeker"),
        ("organization", "Organization"),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default="job_seeker")

class Organization(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    website = models.URLField(blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class JobPost(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Application(models.Model):
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    cover_letter = models.TextField()
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job_post', 'applicant')

    def __str__(self):
        return f"{self.applicant.username}'s application for {self.job_post.title}"
