from django.test import TestCase
from django.urls import reverse
from .models import User, Organization, JobPost, Application

class CoreViewsTest(TestCase):
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_jobseeker_signup_view(self):
        response = self.client.get(reverse('jobseeker_signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup_form.html')

    def test_organization_signup_view(self):
        response = self.client.get(reverse('organization_signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup_form.html')

class UserModelTest(TestCase):
    def test_create_jobseeker(self):
        user = User.objects.create_user(username='testuser', password='password', user_type='job_seeker')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.user_type, 'job_seeker')

    def test_create_organization(self):
        user = User.objects.create_user(username='testorg', password='password', user_type='organization')
        org = Organization.objects.create(user=user, name='Test Corp')
        self.assertEqual(user.username, 'testorg')
        self.assertEqual(user.user_type, 'organization')
        self.assertEqual(org.name, 'Test Corp')

class JobPostModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testorg', password='password', user_type='organization')
        self.organization = Organization.objects.create(user=user, name='Test Corp', is_verified=True)

    def test_create_job_post(self):
        job_post = JobPost.objects.create(
            organization=self.organization,
            title='Test Job',
            description='Test description',
            requirements='Test requirements',
            location='Test location'
        )
        self.assertEqual(job_post.title, 'Test Job')
        self.assertEqual(job_post.organization.name, 'Test Corp')

class ApplicationModelTest(TestCase):
    def setUp(self):
        org_user = User.objects.create_user(username='testorg', password='password', user_type='organization')
        self.organization = Organization.objects.create(user=org_user, name='Test Corp', is_verified=True)
        self.job_post = JobPost.objects.create(
            organization=self.organization,
            title='Test Job',
            description='Test description',
            requirements='Test requirements',
            location='Test location'
        )
        self.job_seeker = User.objects.create_user(username='testseeker', password='password', user_type='job_seeker')

    def test_create_application(self):
        application = Application.objects.create(
            job_post=self.job_post,
            applicant=self.job_seeker,
            cover_letter='Test cover letter'
        )
        self.assertEqual(application.applicant.username, 'testseeker')
        self.assertEqual(application.job_post.title, 'Test Job')
