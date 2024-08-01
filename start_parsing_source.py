#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import hashlib
import os
import datetime
import time

import dateparser
from datetime import timedelta

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


def stop_source(sources_item, attempt=0):
    try:
        sources_item.taken = 0
        sources_item.save(update_fields=['taken'])
    except Exception as e:
        print(e)
        attempt += 1
        if attempt < 6:
            time.sleep(5)
            stop_source(sources_item, attempt=attempt)


def update_only_time(task, attempt=0):
    try:
        task.last_modified = update_time_timezone(timezone.localtime())
        task.save(update_fields=['last_modified'])
    except Exception as e:
        print(f"update_only_time {e}")
        attempt += 1
        if attempt < 6:
            update_only_time(task, attempt=attempt)


def stop_source(sources_item, attempt=0):
    try:
        sources_item.taken = 0
        sources_item.save(update_fields=['taken'])
    except Exception as e:
        print(e)
        attempt += 1
        if attempt < 6:
            time.sleep(5)
            stop_source(sources_item, attempt=attempt)


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
    from core.models import DzenUser, UserDescription, Post, PostContent, Sources, SourcesItems
    from django.db.models import Q
    from dzen.parsing_key import searchy_id

    print("1")

    sources_item = None
    while True:
        try:
            select_sources = Sources.objects.filter(
                Q(retro_max__isnull=True) | Q(retro_max__gte=timezone.now()), published=1,
                status=1)
            print("2")

            sources_item = SourcesItems.objects.filter(network_id=11, disabled=0, taken=0,
                                                       source_id__in=list(select_sources.values_list('id', flat=True))) \
                .order_by('last_modified').first()
            print("3")

            print(f"sources_item {sources_item}")

            if sources_item is not None:
                time_s = select_sources.get(id=sources_item.source_id).sources
                if time_s is None:
                    time_s = 0
                print(2)

                if sources_item.last_modified is None or (
                        sources_item.last_modified + datetime.timedelta(minutes=time_s) <
                        update_time_timezone(timezone.localtime())):
                    sources_item.taken = 1
                    sources_item.save()
                    print(3)

                    list_resp = searchy_id(requests.session(), sources_item.data)
                    user_models = []
                    user_description_models = []
                    post_models = []
                    post_content_models = []
                    print(4)

                    for l in list_resp:
                        source = l['source']
                        try:
                            user_models.append(
                                DzenUser(
                                    id=abs(int(source['id'])),
                                    dzen_id=source['publisher_id'],
                                    screen_name=source['url'],
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
                                    description=source.get('description', ""),
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
                                print(abs(int(l['id'])))
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
                                    url=l['share_link'],
                                    title=l.get("title", "")
                                )
                            )
                        except Exception as e:
                            print(e)
                    django.db.close_old_connections()
                    try:
                        DzenUser.objects.bulk_update(user_models, ['followers', 'last_modified', 'screen_name'], batch_size=200)
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
                        UserDescription.objects.bulk_create(user_description_models, batch_size=200,
                                                            ignore_conflicts=True)
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

                    sources_item.last_modified = update_time_timezone(timezone.localtime())
                    sources_item.taken = 0
                    sources_item.save(update_fields=['taken', 'last_modified'])
            else:
                time.sleep(15 * 60)
        except Exception as e:
            print(e)
            django.db.close_old_connections()
            stop_source(sources_item, attempt=0)
