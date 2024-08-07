#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import hashlib
import os
import datetime

import dateparser

import requests


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
    from django.utils import timezone

    django.setup()
    import pymysql

    pymysql.install_as_MySQLdb()
    from main import searchy_key
    from core.models import DzenUser, UserDescription, Post, PostContent

    # list_resp = searchy_key(requests.session(), "auto")
    list_resp = searchy_key(requests.session(), "россия")
    user_models = []
    user_description_models = []
    post_models = []
    post_content_models = []


    for l in list_resp:
        source = l['source']
        try:
            l.get['socialInfo']['likesCount']
        except Exception:
            pass
        try:
            user_models.append(
                DzenUser.objects.create(
                    id=abs(int(source['id'])),
                    dzen_id=source['publisher_id'],
                    screen_name=source['url'],
                    followers=source['subscribers'],
                    # sphinx_id=get_sphinx_id(source['feed_share_link']),
                    name=source['title'],
                    avatar=source['logo'],
                    # is_verified=source['is_verified'],
                )
            )
        except Exception as e:
            print(e)
            print()
        try:
            user_description_models.append(
                UserDescription.objects.create(
                    id=abs(int(source['id'])),
                    description=source['description'],
                    url=source['feed_share_link']

                )
            )
        except Exception as e:
            print(f"{e}  {source['id']}")

        if "/b/" in l['share_link']:
            try:
                post_models.append(
                    Post.objects.create(
                        id=abs(int(l['id'])),
                        created_date=dateparser.parse(l['creation_time']),
                        owner_id=abs(int(source['id'])),
                        # last_modified=update_time_timezone(timezone.localtime()),
                        likes=l.get('socialInfo', {}).get('likesCount', 0),
                        comments=l.get('socialInfo', {}).get('commentCount', 0),
                        # content_hash=get_md5(l['text'])
                    )
                )
            except Exception as e:
                print(e)

        else:
            try:
                post_models.append(
                    Post.objects.create(
                        id=abs(int(l['id'])),
                        created_date=dateparser.parse(l['creation_time']),
                        owner_id=abs(int(source['id'])),
                        likes=l.get('socialInfo', {}).get('likesCount', 0),
                        comments=l.get('socialInfo', {}).get('commentCount', 0),
                    )
                )
            except Exception as e:
                print(e)
        try:
            post_content_models.append(
                PostContent.objects.create(
                    id=abs(int(l['id'])),
                    content=l['text'],
                    url=l['share_link'],
                    title=l.get("title", "")
                )
            )
        except Exception as e:
            print(e)