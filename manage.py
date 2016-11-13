#!/usr/bin/env python
import json
import os
import sys

if __name__ == '__main__':
    try:
        with open('env.json', 'r') as env_file:
            for key, value in json.loads(env_file.read()).items():
                os.environ.setdefault(key, value)
    except FileNotFoundError:
        raise Exception('env.json should be present and contain configuration')

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kreditiki.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
