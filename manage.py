#!/usr/bin/env python
import json
import os
import sys

if __name__ == "__main__":
    try:
        with open('env.json', 'r') as env_file:
            for key, value in json.loads(env_file.read())['env_vars'].items():
                os.environ[key] = value
    except FileNotFoundError:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kreditiki.settings.dev_settings")
        os.environ.setdefault("LOG_ROOT", "")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
