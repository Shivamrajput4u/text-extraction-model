import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_ocr_project.settings')
application = get_wsgi_application()
