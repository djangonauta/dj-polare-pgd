#!/usr/bin/env python3
import invoke


@invoke.task(default=True)
def run_server(c, settings='development', port=8000):
    cmd = f'./manage.py runserver 0.0.0.0:{port} --settings=projeto.settings.{settings}'
    c.run(cmd, echo=True, pty=True)
