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

    list_resp = searchy_key(requests.session(), "auto")
    user_models = []
    user_description_models = []
    post_models = []
    post_content_models = []
    for l in list_resp:
        source = l['source']

        try:
            user_models.append(
                DzenUser.objects.create(
                    id=(int(source['id'])),
                    screen_name=source['publisher_id'],
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
                    id=(int(source['id'])),
                    description=source['description'],
                    url=source['feed_share_link']

                )
            )
        except Exception as e:
            print(f"{e}  {source['id']}")
        #
        # if "/b/" in l['share_link']:
        #     try:
        #         post_models.append(
        #             Post.objects.create(
        #                 id=l['id'],
        #                 created_date=dateparser.parse(l['creation_time']),
        #                 owner_id=source['id'],
        #                 likes=l['socialInfo']['likesCount'],
        #                 last_modified=update_time_timezone(timezone.localtime()),
        #                 comments=l['socialInfo']['commentCount'],
        #                 url=l['share_link'],
        #                 content_hash=get_md5(l['text'])
        #             )
        #         )
        #     except Exception as e:
        #         print(e)
        #     try:
        #         post_content_models.append(
        #             PostContent.objects.create(
        #                 id=l['id'],
        #                 text=l['text']
        #             )
        #         )
        #     except Exception as e:
        #         print(e)
        # else:
        #     try:
        #         post_models.append(
        #             Post.objects.create(
        #                 id=l['id'],
        #                 created_date=dateparser.parse(l['creation_time']),
        #                 owner_id=source['id'],
        #                 likes=l['socialInfo']['likesCount'],
        #                 comments=l['socialInfo']['commentCount'],
        #                 url=l['share_link'],
        #             )
        #         )
        #     except Exception as e:
        #         print(e)
