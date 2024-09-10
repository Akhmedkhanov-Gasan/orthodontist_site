#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.core.management import execute_from_command_line

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orthodontist_site.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orthodontist_site.settings')  # Убедись, что 'orthodontist_site' — это название твоего проекта

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    port = os.environ.get('PORT', '8000')
    if os.environ.get('DJANGO_DEVELOPMENT', 'true').lower() in ['true', '1']:
        # Использовать 127.0.0.1 для локальной разработки
        execute_from_command_line([sys.argv[0], 'runserver', '127.0.0.1:' + port])
    else:
        # Использовать 0.0.0.0 для развертывания
        execute_from_command_line([sys.argv[0], 'runserver', '0.0.0.0:' + port])
