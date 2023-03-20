#!/usr/bin/env python3
import os
import sys

from django.core import management

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto.settings')
management.execute_from_command_line(sys.argv)
