#!/usr/bin/env python
import json
import os
import sys

if __name__ == "__main__":
    try:
        with open('env.json', 'r') as env_file:
            for key, value in json.loads(env_file.read()).items():
                os.environ.setdefault(key, value)
    except FileNotFoundError:
        # TODO It defaults to DEVELOPMENT mode, but shouldn't
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kreditiki.settings.dev_settings")
        os.environ.setdefault("LOG_ROOT", "")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
