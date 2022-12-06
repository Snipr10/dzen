import json
from bs4 import BeautifulSoup


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
