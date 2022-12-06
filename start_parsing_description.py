#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import hashlib
import os
import datetime

import dateparser

import requests

from django.utils import timezone


def get_md5(text):
    m = hashlib.md5()
    m.update(text.encode())
    return m.hexdigest()


def get_sphinx_id(url):
    return int(str(int(get_md5(url)[:16], 16)))


def update_time_timezone(my_time):
    return my_time + datetime.timedelta(hours=3)


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dzen.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    print(1)
    import django

    django.setup()
    import pymysql
    from main import get_post_info

    pymysql.install_as_MySQLdb()
    from core.models import Post, PostContent

    post_models = []
    post_content_models = []
    for p in Post.objects.filter(last_modified__lte=datetime.date(2000, 1, 1)):
        try:
            text, images = get_post_info(requests.session(), PostContent.objects.get(id=p.id).url)
            p.content_hash = get_md5(text)
            p.last_modified = timezone.now()
            post_models.append(p)
            post_content_models.append(PostContent(id=p.id, content=text))
        except Exception as e:
            print(e)
    try:
        Post.objects.bulk_update(post_models, ['content_hash', 'last_modified'], batch_size=200)
    except Exception as e:
        print(f"Post: {e}")
    try:
        PostContent.objects.bulk_update(post_content_models, ['content'], batch_size=200)
    except Exception as e:
        print(f"Post: {e}")
