# This is a sample Python script.
import requests
import json
import http.client
import json
from bs4 import BeautifulSoup


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# import json
# import re
# import datetime
# from os import walk
# import random
#
# import requests
# from requests import session
#
#
# def compare_amounts(t1, t2):
#     if t1.get("type") != t2.get("type"):
#         return False
#     if t1.get("category") != t2.get("category"):
#         return False
#     amount_1 = float(t1.get("amount"))
#     amount_2 = float(t2.get("amount"))
#
#     if amount_1 * amount_2 >= 0 and abs(amount_1 - amount_2) < abs(amount_1 * (2 / 100)):
#         return True
#     return False
#
#
# def compare_dates(date_1, date_2, date_range):
#     if max(0, date_range.total_seconds()-datetime.timedelta(days=2).total_seconds())  \
#             < (date_1-date_2).total_seconds() < date_range.total_seconds()+datetime.timedelta(days=2).total_seconds():
#         return True
#     return False
#
#
# def add_to_rec_tran(rec_tran, rec_transaction):
#     if len(rec_tran) > 2:
#         is_exist = False
#         for ts in rec_transaction:
#             if all(elem in ts for elem in rec_tran):
#                 is_exist = True
#                 break
#         if not is_exist:
#             rec_transaction.append(rec_tran)
#

#
#
# def get_regions():
#     with open('file.txt') as f:
#         lines = f.readlines()
#     res = []
#     for l in lines:
#         s = l.split("\t")
#         for k in s:
#             res.append(k.strip())
#     return res
#
# def request(query):
#     # query = "Путин"
#     url = f"https://api.vedomosti.ru/v2/documents/search?query={query}&sort=date&date_from=2022-09-08&date_to=2022-09-19&limit=0&from=0"
#
#     payload = {}
#     headers = {
#         'authority': 'api.vedomosti.ru',
#         'accept': 'application/json, text/plain, */*',
#         'accept-language': 'ru-RU,ru;q=0.9',
#         'cache-control': 'no-cache',
#         'dnt': '1',
#         'origin': 'https://www.vedomosti.ru',
#         'pragma': 'no-cache',
#         'referer': 'https://www.vedomosti.ru/',
#         'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
#         'sec-ch-ua-mobile': '?1',
#         'sec-ch-ua-platform': '"Android"',
#         'sec-fetch-dest': 'empty',
#         'sec-fetch-mode': 'cors',
#         'sec-fetch-site': 'same-site',
#         'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Mobile Safari/537.36',
#         'x-access-token': '436301d248649442f5f5fa5f26b9f2daefa68f5c',
#     }
#
#     response = requests.request("GET", url, headers=headers, data=payload)
#     print(f"""{query} - {response.json().get("stat", {}).get("total", None)}""")
#     print(datetime.datetime.now())
#     return response.ok
# if __name__ == '__main__':
#     import instagram_scraper
#
#     args = {"login_user": "goikoananiemann", "login_pass": "hetaeIC2"}
#
#     insta_scraper = instagram_scraper.InstagramScraper(**args)
#     insta_scraper.session.proxies = proxies
#     insta_scraper.authenticate_with_login()
#     shared_data = insta_scraper.query_hashtag_gen(username='SCRAPED_USERNAME')
#     with open('html.txt') as f:
#         lines = f.readlines()
#     res = set()
#     for l in lines:
#         l = l.strip()
#         if "https://tgstat.ru/channel/" in l:
#             res.add(l[l.find("https://tgstat.ru/channel/")+26:l.find("/stat")])
#     for r in res:
#         if "@" in r:
#             r = r.replace("@", " https://t.me/")
#             print(r)
#     print(res)
#     i = 0
#     k = 0
#     while True:
#         try:
#             with open('keys.txt') as f:
#                 lines = f.readlines()
#             random.shuffle(lines)
#             for r in lines:
#                 try:
#                     request(r.strip())
#                 except Exception as e:
#                     print(e)
#                 print(k)
#                 k += 1
#         except Exception as e:
#             k += 1
#             print(e)
#         try:
#             reg = get_regions()
#             random.shuffle(reg)
#
#             for r in reg:
#                 try:
#                     request(r)
#                 except Exception as e:
#                     print(e)
#                 print(k)
#                 k +=1
#         except Exception as e:
#             k +=1
#             print(e)
#
#         i += 1
#         print(f"iteration{i}")
# # if __name__ == '__main__':
# #
#     import instagram_scraper
# #     import requests
# #     s = session()
# #     s.get("https://meet.google.com/gyi-bjeo-hzh")
# #     p = 'http://{}:{}@{}:{}'.format("GbfRPx", "1RBTrX", "138.128.91.73", "8000")
# #     proxies = {"http": p, "https": p}
# #     args = {"login_user": "goikoananiemann", "login_pass": "hetaeIC2"}
#
#     insta_scraper = instagram_scraper.InstagramScraper(**args)
#     insta_scraper.session.proxies = proxies
#     insta_scraper.authenticate_with_login()
#     shared_data = insta_scraper.query_hashtag_gen(username='SCRAPED_USERNAME')
# #         arr.append(item)
# #
# #     f = open('test.json')
# #
# #     # returns JSON object as
# #     # a dictionary
# #     data = json.load(f)
# #     r = {}
# #     for d in data:
# #         k = ""
# #         for i in d.get("items"):
# #             k += "  " + (i.get("keyword") + "\n\n")
# #         r[d.get("title")] = k
# #     with open('file.txt', 'w') as file:
# #         file.write(json.dumps(r))
# #     for (dirpath, dirnames, filenames) in walk("BBVA"):
# #         for name in filenames:
# #             if "BBVA" in name:
# #                 try:
# #                     get_re_transaction(name)
# #                 except Exception as e:
# #                     print(e)
#

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def get_by_key(session, key, url=None):
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'ru-RU,ru;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',

        'DNT': '1',
        'Origin': 'https://dzen.ru',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',

        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
    }

    if url is None:
        url = f"https://dzen.ru/api/v3/launcher/zen-search?clid=1400&country_code=ru&query={key}"
        response = session.get(url, headers=headers)
    else:

        payload = json.dumps({
            "stats": []
        })
        response = session.post(url, headers=headers, data=payload)
    res = response.json()
    return response.json().get("items"), (res.get("more", {}).get('link', None) or None)


def searchy_key(session, key):
    page = 0
    list_resp = []
    set_res_urls = set()
    next_link = None
    while True:
        res, next_link = get_by_key(session, key, next_link)
        if len(res) <= 1:
            break
        page += 1
        for r in res:
            try:
                link = r['link'].split("?")[0]
            except Exception:
                link = None
            if link and link not in set_res_urls:
                set_res_urls.add(link)
                list_resp.append(r)
    return list_resp


def get_by_id(session, id, url=None):
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'ru-RU,ru;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',

        'DNT': '1',
        'Origin': 'https://dzen.ru',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',

        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
    }

    if url is None:
        url = f"https://dzen.ru/api/v3/launcher/more?country_code=ru&clid=1400&lang=ru&channel_id={id}"
        response = session.get(url, headers=headers)
    else:

        payload = json.dumps({
            "stats": []
        })
        response = session.post(url, headers=headers, data=payload)
    res = response.json()
    return response.json().get("items"), (res.get("more", {}).get('link', None) or None)


def searchy_id(session, id):
    page = 0
    list_resp = []
    set_res_urls = set()
    next_link = None
    while True:
        res, next_link = get_by_id(session, id, next_link)
        if len(res) <= 1:
            break
        page += 1
        for r in res:
            try:
                link = r['link'].split("?")[0]
            except Exception:
                link = None
            if link and link not in set_res_urls:
                set_res_urls.add(link)
                list_resp.append(r)
    print(1)


def get_post_info(session, url):
    images = set()
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'Session_id=noauth:;sso_checked=1;; _yasc=vT7fHpjCkkEnCrjGzfL4AcySHu5WUiCzoMB9xGZqXPdxIxKkaVFlL4s+/dc=',
        'DNT': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
    }
    res = session.get(url, headers=headers)
    text = ''
    if "/video/" not in url:
        soup = BeautifulSoup(res.text, "html.parser")

        allNews = soup.find('div', {'itemprop': 'articleBody'})
        try:
            for p in allNews.findAll("p"):
                text += p.text + "<br> \n"
            for i in allNews.findAll("img", {"class": "article-image-item__image"}):
                try:
                    if i.get("src"):
                        images.add(i.get("src"))
                except Exception:
                    pass
        except Exception:
            print(url)
    else:
        try:
            soup = BeautifulSoup(res.text.encode("iso-8859-1").decode(), "html.parser")
            try:
                text = soup.find("meta", {"name": "description"}).get("content")
            except AttributeError:
                text = ""
            image = soup.find("meta", {"property": "og:image"}).get("content")
            if image:
                images.add(image)
        except Exception:
            print(url)
    return {"text": text, "images": images}


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    searchy_id(requests.session(), "605dbc620fe8a73924a594b5")


    # get_by_key(requests.session(), "auto")
    get_post_info(requests.session(), "https://dzen.ru/b/Y4XHsgYfyCkXRHna")
    list_resp = searchy_key(requests.session(), "auto")
    result = []
    for l in list_resp:
        url = l['share_link']
        if "/b/" in url:
            "text = ''"
            continue
        # if not "media" in url:
        url_data = get_post_info(requests.session(), url)
        result.append(url_data)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
