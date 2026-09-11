"""
WSGI config for ping_me_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ping_me_api.settings")

#: The WSGI application callable for the project.
#:
#: Used by WSGI servers to communicate with Django. This object is referenced
#: by the WSGI server's configuration (e.g., gunicorn, uWSGI, mod_wsgi).
application = get_wsgi_application()
