# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/var/www/u1158541/data/www/ramilpowers.ru/blog')
sys.path.insert(1, '/var/www/u1158541/data/blog_venv/lib/python3.9/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'blog.settings.production'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()