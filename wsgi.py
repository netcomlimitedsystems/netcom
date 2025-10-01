import os
import sys

# Path to your project (repo folder)
path = '/home/netcomlimitedsystems/netcom'
if path not in sys.path:
    sys.path.append(path)

# Activate virtual environment
venv_path = '/home/netcomlimitedsystems/netcom/venv'
activate_this = os.path.join(venv_path, 'bin/activate_this.py')
with open(activate_this) as f:
    exec(f.read(), dict(__file__=activate_this))

# Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'netcom_learning.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
