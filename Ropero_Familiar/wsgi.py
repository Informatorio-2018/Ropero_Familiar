"""
WSGI config for Ropero_Familiar project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""
import os
import sys
sys.path.append('C:/Users/ANACONDA/Bitnami Django Stack projects/Ropero_Familiar')
os.environ.setdefault("PYTHON_EGG_CACHE", "C:/Users/ANACONDA/Bitnami Django Stack projects/Ropero_Familiar/egg_cache")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Ropero_Familiar.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
	
