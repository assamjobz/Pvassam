import os
import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_board.settings')
application = get_wsgi_application()
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(email='admin@example.com').exists():
    User.objects.create_superuser('admin@example.com', 'password')
    print('Superuser with email admin@example.com created.')
else:
    print('Superuser with email admin@example.com already exists.')
