#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import hashlib
import os
import datetime
import time
from json import JSONDecoder

import dateparser
from datetime import timedelta

import regex
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


def extract_json_objects(text, decoder=JSONDecoder()):
    """Find JSON objects in text, and yield the decoded JSON data

    Does not attempt to look for JSON arrays, text, or other JSON types outside
    of a parent JSON object.

    """
    pos = 0
    while True:
        match = text.find('{', pos)
        if match == -1:
            break
        try:
            result, index = decoder.raw_decode(text[match:])
            yield result
            pos = match + index
        except ValueError:
            pos = match + 1


def get_user_info(session, username):
    url = f"https://dzen.ru/{username}"
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'ru-RU,ru;q=0.9',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Referer': 'https://sso.dzen.ru/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-site',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'Cookie': 'zen_sso_checked=1; Session_id=noauth:;sso_checked=1;'
    }

    response = session.get(url, headers=headers)

    pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}')
    res = None
    for res_pattern in [p for p in pattern.findall(response.text) if "publisher_oid" in p]:
        for result in extract_json_objects(res_pattern):
            if "publisher_oid" in str(result):
                res = result
                break
        if res:
            break
    return list(res.get("data").values())[0]

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
                print(4)

                try:
                    print(update_time_timezone(timezone.localtime()) - sources_item.last_modified + datetime.timedelta(
                        minutes=time_s))
                    time.sleep((sources_item.last_modified + datetime.timedelta(minutes=time_s)).second - (
                        update_time_timezone(timezone.localtime())).second)
                except Exception as e:
                    print(f"time.sleep {e}")

                if sources_item.last_modified is None or (
                        sources_item.last_modified + datetime.timedelta(minutes=time_s) <
                        update_time_timezone(timezone.localtime())):
                    sources_item.taken = 1
                    sources_item.save()
                    print(5)
                    try:
                        print(sources_item.data)
                    except Exception as e:
                        print(e)
                    session = requests.session()
                    print(sources_item.data)
                    user_data = get_user_info(session, sources_item.data)
                    print(6)
                    for item in list(user_data['feed']['items'].values()):
                        try:
                            user_source = item['items'][0]['source']
                            break
                        except Exception as e:
                            pass
                    print(7)

                    dzen_id = user_source['publisherId']
                    screen_name = f"id/{dzen_id}"
                    is_id = True
                    try:
                        if screen_name not in user_source['shareLink']:
                            screen_name = user_source['shareLink'].split("/")[-1]
                            is_id = False
                    except Exception:
                        pass
                    if is_id:
                        list_resp = searchy_id(session, dzen_id, is_id)
                    else:
                        list_resp = searchy_id(session, screen_name, is_id)
                    user_models = []
                    user_description_models = []
                    post_models = []
                    post_content_models = []
                    print(8)

                    for l in list_resp:
                        print(list_resp)
                        source = l['source']
                        try:
                            user_models.append(
                                DzenUser(
                                    id=abs(int(source['itemId'])),
                                    dzen_id=source['id'],
                                    screen_name=screen_name,
                                    followers=user_source['subscribers'],
                                    name=source['title'],
                                    avatar=source['image']['logo']
                                )
                            )
                        except Exception as e:
                            print(f"DzenUser {e}")
                        try:
                            user_description_models.append(
                                UserDescription(
                                    id=abs(int(source['itemId'])),
                                    description=source.get('description', ""),
                                    url=l['source']['shareLink']

                                )
                            )
                        except Exception as e:
                            print(f"UserDescription {e}")

                        if l.get('share_link') and "/b/" in l.get('share_link'):
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
                                try:
                                    post_models.append(
                                        Post(
                                            id=abs(int(l['itemId'])),
                                            created_date=dateparser.parse(l['publicationDate']),
                                            owner_id=abs(int(source['itemId'])),
                                            # last_modified=update_time_timezone(timezone.localtime()),
                                            likes=l.get('socialInfo', {}).get('likesCount', 0),
                                            comments=l.get('socialInfo', {}).get('commentCount', 0),
                                            # content_hash=get_md5(l['text'])
                                        )
                                    )
                                except Exception as e:
                                    print(f"Post {e}")

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
                                try:
                                    post_models.append(
                                        Post(
                                            id=abs(int(l['itemId'])),
                                            created_date=dateparser.parse(l['publicationDate']),
                                            owner_id=abs(int(source['itemId'])),
                                            # last_modified=update_time_timezone(timezone.localtime()),
                                            likes=l.get('socialInfo', {}).get('likesCount', 0),
                                            comments=l.get('socialInfo', {}).get('commentCount', 0),
                                            # content_hash=get_md5(l['text'])
                                        )
                                    )
                                except Exception as e:
                                    print(f"Post {e}")
                        try:
                            post_content_models.append(
                                PostContent(
                                    id=abs(int(l['itemId'])),
                                    content=l['text'],
                                    url=l['shareLink'],
                                    title=l.get("title", "")
                                )
                            )
                        except Exception as e:
                            print(f"PostContent {e}")
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
