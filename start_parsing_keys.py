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

    django.setup()
    import pymysql

    pymysql.install_as_MySQLdb()
    from main import searchy_key
    from core.models import DzenUser, UserDescription, Post, PostContent

    list_resp = searchy_key(requests.session(), "spb")
    user_models = []
    user_description_models = []
    post_models = []
    post_content_models = []

    for l in list_resp:
        source = l['source']
        try:
            user_models.append(
                DzenUser(
                    id=abs(int(source['id'])),
                    screen_name=source['publisher_id'],
                    followers=source['subscribers'],
                    name=source['title'],
                    avatar=source['logo'],
                )
            )
        except Exception as e:
            print(e)
        try:
            user_description_models.append(
                UserDescription(
                    id=abs(int(source['id'])),
                    description=source['description'],
                    url=source['feed_share_link']

                )
            )
        except Exception as e:
            print(f"Error {e} {source['feed_share_link']} {source['id']}")

        if "/b/" in l['share_link']:
            try:
                post_models.append(
                    Post(
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
                    Post(
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
                    url=l['share_link']
                )
            )
        except Exception as e:
            print(e)
    try:
        DzenUser.objects.bulk_update(user_models, ['followers', 'last_modified'], batch_size=200)
    except Exception as e:
        print(f"DzenUser: {e}")

    try:
        DzenUser.objects.bulk_create(user_models, batch_size=200, ignore_conflicts=True)
    except Exception as e:
        print(f"DzenUser: {e}")

    try:
        UserDescription.objects.bulk_update(user_description_models, ['description'], batch_size=200)
    except Exception as e:
        print(f"DzenUser: {e}")
    try:
        UserDescription.objects.bulk_create(user_description_models, batch_size=200, ignore_conflicts=True)
    except Exception as e:
        print(f"UserDescription: {e}")

    try:
        Post.objects.bulk_update(post_models, ['likes', 'comments'], batch_size=200)
    except Exception as e:
        print(f"Post: {e}")
    try:
        Post.objects.bulk_create(post_models, batch_size=200, ignore_conflicts=True)
    except Exception as e:
        print(f"Post: {e}")
    try:
        PostContent.objects.bulk_create(post_content_models, batch_size=200, ignore_conflicts=True)
    except Exception as e:
        print(f"PostContent: {e}")
