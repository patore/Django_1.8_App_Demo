#!/usr/bin/env python
import os


if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'dummy_app.settings'

    from django.core.management import execute_from_command_line
    import sys

    execute_from_command_line(sys.argv)
