# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/var/www/u0872810/data/www/cargo.annasoft.site/cargo_project')
sys.path.insert(1, '/var/www/u0872810/data/cargo_env/lib/python3.9/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'cargo_project.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()