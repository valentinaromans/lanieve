import os
import sys

# Añadir la ruta del proyecto a PYTHONPATH
sys.path.append('/home/proyectolanieve/lanieve')
sys.path.append('/home/proyectolanieve/.virtualenvs/venv/lib/python3.10/site-packages')

# Establecer la configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lanieve.settings')

# Obtén la aplicación WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
