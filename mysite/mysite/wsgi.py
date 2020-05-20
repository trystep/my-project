"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os, sys

# add the hellodjango project path into the sys.path
sys.path.append("/home/django/my-project/mysite/")

# add the virtualenv site-packages path to the sys.path
sys.path.append("/home/django/env-my-project/lib/python3.8/site-packages/")

# poiting to the project settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")


from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = get_wsgi_application()
